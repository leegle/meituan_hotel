# coding=utf-8

"""
将文件写入mysql
"""

import os
import config
import pandas as pd
from log_handler import log
from sqlalchemy import create_engine

host = config.host
user = config.user
pwd = config.pwd
db = config.db
table = config.table
table_s = config.table_s


def insert_2_mysql():
    try:
        engine = create_engine('mysql+pymysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(user, pwd, host, db),
                               encoding='utf-8')
        df = pd.read_csv(os.path.abspath(config.ready_2_check_in), sep='\t')
        df.to_sql(table, con=engine, schema=db, if_exists='append', index=False)

        df2 = pd.read_csv(os.path.abspath(config.current_data), sep='\t')
        df2.to_sql(table_s, con=engine, schema=db, if_exists='replace', index=False)
    except Exception as e:
        log.warning('写入数据库出错\t{0}'.format(e))

