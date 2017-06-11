# -*- coding:utf-8 -*-
#  author: yukun
import requests
import pymongo
import time
from config import *
from bs4 import BeautifulSoup

client = pymongo.MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]

headers  = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Connection':'keep-alive'
}
loginData={
    'username' : USERNAME,
    'password' : PASSWORD,
    'userlogin' : "true",
}
s = requests.Session()
login_url = 'https://passport.lagou.com/login/login.html?ts=1497162442867&serviceId=lagou&service=https%253A%252F%252Fwww.lagou.com%252F&action=login&signature=72A4603E1EEBEAFA295397B4E53ED7D9'
s.post(login_url, data=loginData, headers=headers)

def parse_link(url, pages):
    link = '{}{}/?filterOption=3'.format(url, str(pages))
    resp = s.get(link, headers=headers)
    time.sleep(1)
    if resp.status_code == 404:
        pass
    else:
        soup = BeautifulSoup(resp.text, 'lxml')

        positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h2')
        adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
        publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')
        moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')
        needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')
        companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
        tags = []
        if soup.find('div', class_='li_b_l'):
            tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')
        fulis = soup.select('ul > li > div.list_item_bot > div.li_b_r')

        for position,add,publish,money,need,company,tag,fuli in \
                zip(positions,adds,publishs,moneys,needs,companys,tags,fulis):
            data = {
                'position' : position.get_text(),
                'add' : add.get_text(),
                'publish' : publish.get_text(),
                'money' : money.get_text(),
                'need' : need.get_text().split('\n')[2],
                'company' : company.get_text(),
                'tag' : tag.get_text().replace('\n','-'),
                'fuli' : fuli.get_text()
            }
            if db[MONGO_TABLE].insert_one(data):
                print('保存数据库成功', data)
