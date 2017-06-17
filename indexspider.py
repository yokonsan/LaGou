# -*- coding:utf-8 -*-
#  author: yukun
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	try:
		resp = requests.get(url, headers=headers)
		if resp.status_code == 200:
			print('ok')
			return resp.text
		return None
	except RequestException:
		return None

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
	return datas
