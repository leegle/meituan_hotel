# coding=utf8

"""
    针对出现验证的情况，发送短信验证
"""

import json
import time
import random
import config
import requests
from log_handler import log


url = 'https://api.mysubmail.com/message/send'


data = {
    'appid': config.appid,
    'to': config.tel_num,
    'content': '【EXLC】请在10分钟内处理异常。',
    'signature': config.signature
}


def send_rescue_msg():
    """直接调用"""
    retry = 5
    while retry > 0:
        try:
            response = requests.post(url=url, data=data, timeout=30)
            if response.status_code < 300:
                js_dict = json.loads(response.content.decode('utf-8'))
                status = js_dict.get('status')
                if status == 'success':
                    log.debug('完成短信api调取，并发送短信')
                    break
            time.sleep(random.randint(1, 3))
        except Exception as e:
            log.warning('在调用短信接口时候发生错误\t{0}'.format(e))
            time.sleep(random.randint(10, 30))

        retry -= 1
    return
