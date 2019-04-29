# coding=utf-8


"""
    作为美团数据采集的入口
    执行逻辑：
        每5秒钟调用一次爬虫
        每次调用前，对 meituan_cookie.txt 内容进行提取，如果遇到内容为0，即认为该cookie已经失效

    采集到的数据，放入ready_2_checkin.csv, all_record.csv 里

"""

import os
import random
import config
import time
from call_rescue import send_rescue_msg
from log_handler import log
from meituan_spider import receive_cookie_and_start
from mysql_handler import insert_2_mysql


def run():
    # 检测cookie
    log.debug('初始化:\t读取文件里cookie,准备抓取数据')
    cookie_ctx = open(os.path.abspath(config.meituan_cookie), 'r', encoding='utf-8').read()
    if cookie_ctx != '0':
        # 证明cookie失效，需要更新新的cookie
        # log汇报
        log.debug('cookie不为"0"，调用爬虫')
        # 调度爬虫
        # 将文件重置
        initial_data_file()
        receive_cookie_and_start(cookie_ctx)
        # 写入数据库
        insert_2_mysql()
        log.debug('完成写入数据库')
    else:
        log.warning('Cookie目录文件Cookie无效，调用短信接口')
        # 发短信提醒
        send_rescue_msg()


def initial_data_file():
    with open(os.path.abspath(config.ready_2_check_in), 'w', encoding='utf-8') as f:
        f.write('\t'.join(['orderId', 'poiName', 'roomName', 'roomCount', 'guest', 'orderStatus',
                           'paytime', 'paytime_c', 'price', 'realFloorPrice', 'rpInfo', 'checkInDate',
                           'checkInDate_c', 'checkOutDate', 'checkOutDate_c']) + '\n')


def schedule():
    # 主程序
    while True:
        sleep_time = random.randint(500, 600)
        start = time.time()
        run()
        end = time.time()
        if end-start < sleep_time:
            sleeping = sleep_time - (end - start)
            log.debug('此次休眠:\t{0}秒'.format(sleeping))
            time.sleep(sleeping)


if __name__ == '__main__':
    schedule()