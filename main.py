# -*- coding:utf-8 -*-
#  author: yukun
import time
from multiprocessing import Pool
from spider import parse_link
from indexspider import parse_index

def main(data):
    url = data['url']
    print(url)
    mongo_table = data['name']
    if mongo_table[0] == '.':
        mongo_table = mongo_table[1:]
    parse_link(url, mongo_table)


if __name__ == '__main__':
    t1 = time.time()

    pool = Pool(processes=4)

    datas = (data for data in parse_index())
    pool.map(main, datas)
    pool.close()
    pool.join()

    print(time.time() - t1)
