# coding=utf-8

"""
    负责修改cookie目录里的cookie

"""

import os
import config
from log_handler import log

cookie_file = config.meituan_cookie


def receive_cookie_and_reload(cookie_ctx):
    with open(os.path.abspath(cookie_file), 'w', encoding='utf-8') as f:
        f.write(cookie_ctx)
    log.debug('新cookie装载完毕')


def reload_cookie_file():
    # 重置Cookie
    file = os.path.abspath(config.meituan_cookie)
    with open(file, 'w', encoding='utf-8') as f:
        f.write('0')