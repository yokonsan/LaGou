# -*- coding:utf-8 -*-
#  author: yukun
import requests
import pymongo
from config import *
from bs4 import BeautifulSoup

client = pymongo.MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]

headers  = {
    'Cookie':'user_trace_token=20170603115043-d0c257a054ee44f99177a3540d44dda1; LGUID=20170603115044-d1e2b4d1-480f-11e7-96cf-525400f775ce; JSESSIONID=ABAAABAAAGHAABHAA8050BE2E1D33E6C2A80E370FE9167B; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; _ga=GA1.2.922290439.1496461627; X_HTTP_TOKEN=3876430f68ebc0ae0b8fac6c9f163d45; _ga=GA1.3.922290439.1496461627; LGSID=20170720174323-df1d6e50-6d2f-11e7-ac93-5254005c3644; LGRID=20170720174450-12fc5214-6d30-11e7-b32f-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500541369; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500543655',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}


def parse_link(url, MONGO_TABLE):
    for page in range(1, 31):
        link = '{}{}/?filterOption=3'.format(url, str(page))
        resp = requests.get(link, headers=headers)
        if resp.status_code == 404:
            pass
        else:
            soup = BeautifulSoup(resp.text, 'lxml')

            positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
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
                save_database(data, MONGO_TABLE)

def save_database(data, MONGO_TABLE):
    if db[MONGO_TABLE].insert_one(data):
        print('保存数据库成功', data)
