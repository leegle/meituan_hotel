# coding=utf-8


# 爬虫

url = 'https://eb.meituan.com/api/v1/ebooking/orders'
url_ol = 'https://eb.meituan.com/api/v1/ebooking/common/loginfo/orderList'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'eb.meituan.com',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://eb.meituan.com/ebk/consume/order.html?tab=checkin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

params = {
    'endTime': '1556035199999',
    'filter': 'READY_TO_CHECKIN',
    'invoiceMark': '0',
    'limit': '0',
    'offset': '10',
    'orderId': '',
    'orderStatus': '',
    'orderType': '4,7',
    'partnerId': '',
    'phone': '',
    'poiId': '',
    'roomIds': '',
    'searchTimeType': '1',
    'sortField': '1',
    'sortType': '2',
    'startTime': '1555948800000',
    'zlPois': '',
}

params_ol = {
    '_token': ''
}


# 文件目录

# meituan_cookie = './Data/meituan_cookie.txt'
meituan_cookie = './cookie/cookie.txt'

ready_2_check_in = './Data/ready_2_checkin.csv'

all_record = './Data/all_record.csv'

html_record = './Data/html_record.txt'

id_set = './Data/id_set.txt'


# mysql 配置

host = '120.25.149.160'
user = 'spider'
pwd = 'spider2014'
db = 'spider'
# table = 'ready_2_check_in'
table = 'new_ready_2_check_in'


# 短信的配置

tel_num = 18200120030

appid = '26684'
signature = '40350721c82299f878575fc15b9dc171'

