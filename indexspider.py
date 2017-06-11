# -*- coding:utf-8 -*-
#  author: yukun
import requests
from bs4 import BeautifulSoup


def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	resp = requests.get(url, headers=headers).text

	return resp

def parse_index():
	url = 'https://www.lagou.com/'
	soup = BeautifulSoup(get_html(url), 'lxml')
	all_positions = soup.select('div.menu_sub.dn > dl > dd > a')
	datas = []
	joburls = [i['href'] for i in all_positions]
	jobnames = [i.get_text() for i in all_positions]

	for joburl, jobname in zip(joburls, jobnames):
		data = {
			'url' : joburl,
			'name' : jobname
		}
		datas.append(data)
	print(datas)
	return datas

parse_index()