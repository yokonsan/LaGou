# -*- coding:utf-8 -*-
#  author: yukun
import time
from config import MONGO_TABLE
from multiprocessing import Pool
from spider import parse_link
from indexspider import parse_index


def get_alllink_data():
    for i in parse_index():
        if i['name'] == MONGO_TABLE:
            url = i['url']
            print(url)
            for i in range(1, 31):
                parse_link(url, i)

if __name__ == '__main__':
    t1 = time.time()

    pool = Pool(processes=4)
    pool.apply_async(get_alllink_data)
    pool.close()
    pool.join()

    print(time.time() - t1)