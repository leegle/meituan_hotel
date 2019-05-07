# coding=utf-8


"""
    爬虫模块
    请求数据，解析数据, 存储数据

"""


import os
import requests
import config
import time
import json
import datetime
from call_rescue import send_rescue_msg
from copy import deepcopy
from log_handler import log
from token_killer import parse_token
from cookie_handler import reload_cookie_file

# 创建一个session
session = requests.Session()


def receive_cookie_and_start(cookie_ctx):
    # 拿到cookie后，开始请求
    get_data(cookie_ctx)


def get_data(cookie):
    cookie = {'Cookie': cookie}
    page, total_page = 0, 0
    url = config.url
    url_ol = config.url_ol
    params_ol = config.params_ol
    headers = config.headers
    while page <= total_page:
        # 先请求一次 orderList
        params_ol.update({'_token': parse_token()})
        html_ol = do_request(url_ol, headers, params_ol, cookie)
        log.debug('请求order_list结果:\t{0}'.format(html_ol))
        params = construct_params()
        params.update({'limit': str(page*10)})
        html = do_request(url, headers, params, cookie)
        if html != 'null_page':
            js_dict = loads_json(html)
            # 保存页面
            save_page(js_dict)
            if js_dict is not None:
                # 判断状态, 成功 status:0 , 失败 status: 303
                if deal_status(js_dict):
                    log.info('请求结果发现Cookie已经过期，请重新载入cookie')
                    # 将cookie文档变为0
                    send_rescue_msg()
                    reload_cookie_file()
                    break
                log.debug('当前cookie有效, 开始解析html')
                if page == 0:
                    count = get_total_count(js_dict)
                    total_page = int(count/10) + 1 if count/10 > int(count/10) else int(count/10)
                    log.debug('本次请求有\t{}\t页数据'.format(total_page))
                    total_page -= 1
                # 获取数据
                data = do_parase(js_dict)
                # 保存数据
                if data:
                    save_data(data)
        time.sleep(5)
        page += 1

    log.debug('本次抓取完毕')


def deal_status(js_dict):
    # 处理状态码
    status = js_dict.get('status')
    if status != 0:
        return True


def save_page(js_dict):
    # 保存当前的html结果
    page = deepcopy(js_dict)
    file = config.html_record
    page.update({'crawlTime': datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')})
    with open(file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(page, ensure_ascii=False) + '\n')
    log.debug('已保存当前页面html')


def get_total_count(js_dict):
    # 获取总数据量
    return js_dict.get('data').get('total')


def do_parase(js_dict):
    # 解析数据
    data = []
    for each in js_dict.get('data').get('results'):
        # 订单号
        orderId = str(each.get('orderId'))
        # 酒店名称
        poiName = each.get('poiName').replace('\t', ' ')
        # 房间
        roomName = each.get('roomName').replace('\t', ' ')
        # 房间数量
        roomCount = str(each.get('roomCount'))
        # 客人
        guest = ','.join([i.get('name') for i in each.get('guests')])
        # 状态
        status = each.get('status')
        # 购买时间
        # paytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(each.get('payTime')/1000)))
        paytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(each.get('aptCreatTime')/1000)))
        paytime_c = str(each.get('aptCreatTime'))
        # 美团价
        # commission = str(each.get('commission')/10)
        price = str(each.get('price')/100)
        # 最低价
        realFloorPrice = str(each.get('realFloorPrice')/100)
        # info
        rpInfo = each.get('rpInfo')
        # 入住日期
        checkInDate = time.strftime('%Y-%m-%d', time.localtime(int(each.get('checkInDate')/1000)))
        checkInDate_c = str(each.get('checkInDate'))
        # 离店日期
        checkOutDate = time.strftime('%Y-%m-%d', time.localtime(int(each.get('checkOutDate')/1000)))
        checkOutDate_c = str(each.get('checkOutDate'))
        # 新增
        # 采集时间
        input_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        data.append([orderId, poiName, roomName, roomCount, guest, status, paytime, paytime_c, price,
                     realFloorPrice, rpInfo, checkInDate, checkInDate_c, checkOutDate, checkOutDate_c, input_date])
    return data


def save_data(data):
    # 保存数据
    # 需要存3个目录
    id_set = set([i.strip() for i in open(os.path.abspath(config.id_set), 'r', encoding='utf-8')])
    for each in data:
        if each[0] not in id_set:
            with open(os.path.abspath(config.ready_2_check_in), 'a', encoding='utf-8') as f:
                f.write('\t'.join(each) + '\n')
            each.append(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            with open(os.path.abspath(config.all_record), 'a', encoding='utf-8') as g:
                g.write('\t'.join(each) + '\n')

            # 保存id
            with open(os.path.abspath(config.id_set), 'a', encoding='utf-8') as r:
                r.write(each[0] + '\n')
        # 保存current data
        with open(os.path.abspath(config.current_data), 'a', encoding='utf-8') as f:
            f.write('\t'.join(each) + '\n')

    log.debug('完成数据清洗并写入本地')


def loads_json(html):
    json_dict = None
    try:
        json_dict = json.loads(html)
    except Exception as e:
        log.warning('解析json出错\t{0}\n该json为\t{1}'.format(e, html))
    return json_dict


def construct_params():
    # 拼装参数, 主要是拼装时间
    params = deepcopy(config.params)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    startTime = ''.join([str(int(time.mktime(time.strptime('{0} 00:00:00'.format(today), '%Y-%m-%d %H:%M:%S')))), '000'])
    endTime = ''.join([str(int(time.mktime(time.strptime('{0} 23:59:59'.format(today), '%Y-%m-%d %H:%M:%S')))), '999'])
    params.update({'startTime': startTime, 'endTime': endTime})
    params.update({'_token': parse_token()})
    return params


def do_request(url, headers, params, cookie):
    # 简易的请求模块
    # 重试次数为3次
    retry = 3
    html = 'null_page'
    while retry > 0:
        try:
            response = session.get(url=url, headers=headers, params=params, cookies=cookie, timeout=30)
            status_code = response.status_code
            if status_code < 300:
                html = response.content.decode('utf-8')
                break
        except Exception as e:
            log.info('请求出错\t{0}'.format(e))
            time.sleep(10)
        retry -= 1
    return html
