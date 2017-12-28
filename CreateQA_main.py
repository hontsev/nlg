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

db_patent='ana_des_20171121'

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
        # db_conn.close()
        return res

def execute(sql):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(sql)
            db_conn.commit()
    finally:
        pass
        # db_conn.close()

def insert_pair(id,question,answer,author=''):
    execute("INSERT INTO ana_des_result_20171123(id,question,answer,author) VALUES(%s,%s,%s,%s)" % id,question,answer,author)

def add_item(item_list,name,name_list):
    tmp_list = list()
    for item in item_list:
        for new_item in name_list:
            item[name] = new_item
            tmp_list.append(item)
    item_list = tmp_list
    return item_list

def main_deal():
    type_min=1
    type_max=44
    year_min=1900
    year_max=2050
    top_min=1
    top_max=10
    # base_keyword={"【优先权年】"=}

    # 获取来源国字段的可能的取值
    from_country_tmp = select("SELECT distinct 申请人国别代码 FROM %s" % db_patent)
    from_country = list()
    for item in from_country_tmp:
        for country in item['申请人国别代码'].split(','):
            if len(country.strip()) > 0:
                from_country.append(country.strip())
    from_country = list(set(from_country))

    # 获取流向国的可能取值，这里是取得其英文字母编号
    to_country_tmp = select("SELECT distinct SUBSTRING(公开（公告）号,1,2) as 流向国国别代码 FROM %s" % db_patent)
    to_country = list()
    for item in to_country_tmp: to_country.append(item['流向国国别代码'])
    # to_country = list(set(to_country))

    # 领域的可能取值
    field=list()
    field_tmp = select("SELECT distinct 领域 FROM %s" % db_patent)
    for item in field_tmp:field.append(item["领域"])

    # 子领域的可能取值
    sub_field = list()
    sub_field_tmp = select("SELECT distinct 子领域 FROM %s" % db_patent)
    for item in sub_field_tmp: sub_field.append(item["子领域"])

    # 申请人的可能取值
    applicant_tmp = select("SELECT distinct 申请人 FROM %s" % db_patent)
    applicant = list()
    for item in applicant_tmp:
        for name in item['申请人'].split(';'):
            if len(name.strip()) > 0:
                applicant.append(name.strip())
    applicant = list(set(applicant))

    # 发明人的可能取值
    inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
    inventor = list()
    for item in inventor_tmp:
        for name in item['发明人'].split(';'):
            if len(name.strip()) > 0:
                inventor.append(name.strip())
    inventor = list(set(inventor))
    
    for type in range[type_min : type_max]:
        q_template_list=select("SELECT content FROM q_template WHERE type='%s'" % type)
        a_template_list = select("SELECT content FROM a_template WHERE type='%s'" % type)
        if len(q_template_list)<=0 or len(a_template_list)<=0:
            continue

        for q_template in q_template_list:
            base_keyword_list=[{"type":type}]
            # sql="SELECT * FROM ana_des_20171121 "
            # is_first_condition=True;
            if '【优先权年】' in q_template:  add_item(q_template_list,'优先权年',range[year_min:year_max])
            if '【授权年】' in q_template:  add_item(q_template_list,'授权年',range[year_min:year_max])
            if '【申请年】' in q_template:  add_item(q_template_list, '申请年', range[year_min:year_max])
            if '【来源国】' in q_template:  add_item(q_template_list, '来源国', from_country)
            if '【流向国】' in q_template:  add_item(q_template_list, '流向国', to_country)

            for a_template in a_template_list:
                pass



link_database()
inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
inventor = list()
for item in inventor_tmp:
    for name in item['发明人'].split(';'):
        if len(name.strip()) > 0:
            inventor.append(name.strip())
inventor = list(set(inventor))
print(inventor)
db_conn.close()
# link_database()
# print(select("SELECT * FROM ana_des_20171121 LIMIT 10"))
