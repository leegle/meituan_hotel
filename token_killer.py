# conding=utf-8


import os


def parse_token():
    path = os.path.abspath('./rohr.min.js')
    cmd = "phantomjs {0}".format(path)
    token = os.popen(cmd).read().strip()
    return token
