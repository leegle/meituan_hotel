# coding=utf-8


import logging
import os


def logger():
    log = logging.getLogger(name='meituan_spider')
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.abspath('./Log/meituan.log'))
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log

# 初始化log
log = logger()


def output_log():
    """输出最后30行日志"""
    with open(os.path.abspath('./Log/meituan.log'), 'r') as f:
        txt = f.readlines()
    ctx = ''
    if len(txt) > 30:
        keys = [k for k in range(0, len(txt))]
        result = {k: v for k, v in zip(keys, txt[::-1])}
        ctx_re = [result[i] for i in range(30)]
        ctx_re.reverse()
        for p in ctx_re:
            ctx +=p
    else:
        ctx = ''.join(txt)
    return ctx

