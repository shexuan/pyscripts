#!usr/bin/env python3
# -*- coding:utf-8 -*-


'''
Usage:
with Mysql(host,port,user,passwd,db,charset) as cursor:
    print(cursor.fetchone())
'''


from contextlib import contextmanager
import pymsql


@contextmanager
def Mysql(host, port, user, passwd, db, charset='utf-8'):
    conn = pymsql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()
