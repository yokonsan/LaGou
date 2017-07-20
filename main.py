# -*- coding:utf-8 -*-
#  author: yukun
import time
from multiprocessing import Pool
from spider import parse_link
from indexspider import parse_index

def main(pages):
    datas = parse_index()
    for i in datas:
        url = i['url']
        print(url)
        mongo_table = i['name']
        if mongo_table[0] == '.':
            mongo_table = mongo_table[1:]
        parse_link(url, pages, mongo_table)


if __name__ == '__main__':
    t1 = time.time()

    pool = Pool(processes=4)

    pages = ([p for p in range(1, 31)])
    pool.map(main, pages)
    pool.close()
    pool.join()

    print(time.time() - t1)
