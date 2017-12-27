# -*- coding: UTF-8 -*-
# author: zhangyao
# data: 2017/12/27
# function: 问答生成主入口程序
# input:
# output:

import pymysql
import json

db_config_file = "db_config"
db_conn = object()


# 连接数据库
def link_database():
    try:
        config_file=open(db_config_file,mode='r',encoding="utf-8")
        config_str=config_file.read()
        config=json.loads(config_str)
        config['charset']='utf8'
        global db_conn
        db_conn=pymysql.connect(**config)
        setattr(db_conn, "cursorclass", pymysql.cursors.DictCursor)
    finally:
        pass
        # print(config)

def select(sql):
    try:
        with db_conn.cursor() as cursor:
            # 执行sql语句，插入记录
            cursor.execute(sql)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            res = cursor.fetchall()
            db_conn.commit()
    finally:
        db_conn.close()
        return res

def execute(sql):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(sql)
            db_conn.commit()
    finally:
        db_conn.close()

def insert_pair(id,question,answer,author=''):
    execute("INSERT INTO ana_des_result_20171123(id,question,answer,author) VALUES(%s,%s,%s,%s)" % id,question,answer,author)

def main_deal():
    type_min=1
    type_max=44
    year_min=1900
    year_max=2050






link_database()
# print(select("SELECT * FROM ana_des_20171121 LIMIT 10"))
