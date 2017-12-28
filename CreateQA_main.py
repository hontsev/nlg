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

code_dir = dict()

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
            output_item=dict()
            for i in item:output_item[i]=item[i]
            output_item[name] = new_item
            tmp_list.append(output_item)
    # item_list = tmp_list
    # print(item_list)
    return tmp_list

def set_sql(item):
    sql="SELECT * FROM %s" % db_patent
    is_first_condition = True
    if '优先权年' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "((SUBSTR(SUBSTRING_INDEX(优先权信息,';',1),-8,4)+0<=SUBSTR(SUBSTRING_INDEX(优先权信息,';',-1),-8,4)+0 and SUBSTR(SUBSTRING_INDEX(优先权信息,';',1),-8,4)='%s') or (SUBSTR(SUBSTRING_INDEX(优先权信息,';',1),-8,4)+0>SUBSTR(SUBSTRING_INDEX(优先权信息,';',-1),-8,4)+0 and SUBSTR(SUBSTRING_INDEX(优先权信息,';',-1),-8,4)='%s'))" % \
               (item['优先权年'],item['优先权年'])
    if '授权年' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "(`专利类型`='发明授权'or'实用新型'or'外观设计') and SUBSTR(`公开（公告）日`,1,4)='%s'" % item['授权年']
    if '申请年' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "substr(`申请日`,1,4)='%s'" % item['申请年']
    if '来源国' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "`申请人国别代码`='%s'" % item['来源国']
    if '流向国' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "SUBSTRING(`公开（公告）号`,1,2)='%s'" % item['流向国']
    if '领域' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "`领域`='%s'" % item['领域']
    if '子领域' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "`子领域`='%s'" % item['子领域']
    if '申请人' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "(`申请人`='%s' or `申请人` REGEXP '^%s[;]+' or `申请人` REGEXP '[;[:space:]]+%s$' or `申请人` REGEXP '[;[:space:]]+%s[;]+')" % \
               (item['申请人'],item['申请人'],item['申请人'],item['申请人'])
    if '发明人' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "(`发明人`='%s' or `发明人` REGEXP '^%s[;]+' or `发明人` REGEXP '[;[:space:]]+%s$' or `发明人` REGEXP '[;[:space:]]+%s[;]+')" % \
               (item['发明人'], item['发明人'], item['发明人'], item['发明人'])
    print(sql)
    return sql

def get_key1(item):
    if '优先权年' in item:
        return str(item['优先权年'])
    else:
        return ''

def get_key2(item):
    if '授权年' in item:
        return str(item['授权年'])
    else:
        return ''

def get_key3(item):
    if '申请年' in item:
        return str(item['申请年'])
    else:
        return ''

def get_key4(item):
    if '来源国' in item:
        return item['来源国']
    else:
        return ''

def get_key5(item):
    if '流向国' in item:
        id=item['流向国'];
        if id in code_dir :
            return code_dir[id]
        else:
            return ''
    else:
        return ''

def get_key6(item):
    if '领域' in item:
        return item['领域']
    else:
        return ''

def get_key7(item):
    if '子领域' in item:
        return item['子领域']
    else:
        return ''

def get_key8(item):
    if '申请人' in item:
        return item['申请人']
    else:
        return ''

def get_key9(item):
    if '发明人' in item:
        return item['发明人']
    else:
        return ''

def get_key10(item):
    if 'topN数目' in item:
        return str(item['topN数目'])
    else:
        return ''

def fill_base_key(template, item):
    result =template

    result =result.replace('【优先权年】', get_key1(item))
    result =result.replace('【授权年】', get_key2(item))
    result =result.replace('【申请年】', get_key3(item))
    result =result.replace('【来源国】', get_key4(item))
    result =result.replace('【流向国】', get_key5(item))
    result =result.replace('【领域】', get_key6(item))
    result =result.replace('【子领域】', get_key7(item))
    result =result.replace('【申请人】', get_key8(item))
    result =result.replace('【发明人】', get_key9(item))
    result =result.replace('【topN数目】', get_key10(item))

    return result

def fill_compute_key(template, item):
    result = template

    return result

def main_deal():
    qa_type_min=1
    qa_type_max=2 # 44

    year_min=2016
    year_max=2017
    top_min=3
    top_max=3
    # base_keyword={"【优先权年】"=}

    # 获取来源国字段的可能的取值
    from_country_tmp = select("SELECT distinct 申请人国别代码 FROM %s" % db_patent)
    from_country = list()
    for item in from_country_tmp:
        for country in item['申请人国别代码'].split(','):
            if len(country.strip()) > 0:
                from_country.append(country.strip())
    from_country = list(set(from_country))[0:2]

    # 获取流向国的可能取值，这里是取得其英文字母编号
    to_country_tmp = select("SELECT distinct SUBSTRING(公开（公告）号,1,2) as 流向国国别代码 FROM %s" % db_patent)
    to_country = list()
    for item in to_country_tmp: to_country.append(item['流向国国别代码'])
    to_country = list(set(to_country))[0:2]

    # 领域的可能取值
    field=list()
    field_tmp = select("SELECT distinct 领域 FROM %s" % db_patent)
    for item in field_tmp:field.append(item["领域"])
    field=field[0:2]

    # 子领域的可能取值
    sub_field = list()
    sub_field_tmp = select("SELECT distinct 子领域 FROM %s" % db_patent)
    for item in sub_field_tmp: sub_field.append(item["子领域"])
    sub_field=sub_field[0:2]

    # 申请人的可能取值
    applicant_tmp = select("SELECT distinct 申请人 FROM %s" % db_patent)
    applicant = list()
    for item in applicant_tmp:
        for name in item['申请人'].split(';'):
            if len(name.strip()) > 0:
                applicant.append(name.strip())
    applicant = list(set(applicant))[0:2]

    # 发明人的可能取值
    inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
    inventor = list()
    for item in inventor_tmp:
        for name in item['发明人'].split(';'):
            if len(name.strip()) > 0:
                inventor.append(name.strip())
    inventor = list(set(inventor))[0:2]
    
    for qa_type in range(qa_type_min, qa_type_max):
        q_template_list= select("SELECT content FROM q_template WHERE `type`='%s'" % qa_type)
        a_template_list = select("SELECT content FROM a_template WHERE `type`='%s'" % qa_type)
        # if len(q_template_list)<=0 or len(a_template_list)<=0:
            # continue
        # q_template_list=[{'content':'【优先权年】【授权年】【申请年】【来源国】【流向国】【领域】【子领域】【申请人】【发明人】【topN数目】'}]
        q_template_list = [{'content': '在【优先权年】，申请年为【申请年】的，从【来源国】向【流向国】的，在【领域】领域的【子领域】子领域中的，由【申请人】申请，并且发明人为【发明人】的专利有哪些？'}]
        for q_template in q_template_list:
            q_template=q_template['content']
            base_keyword_list=[{"type":qa_type}]
            # sql="SELECT * FROM ana_des_20171121 "
            # is_first_condition=True;
            if '【优先权年】' in q_template:  base_keyword_list=add_item(base_keyword_list,'优先权年',range(year_min,year_max))
            if '【授权年】' in q_template:  base_keyword_list=add_item(base_keyword_list,'授权年',range(year_min,year_max))
            if '【申请年】' in q_template:  base_keyword_list=add_item(base_keyword_list, '申请年', range(year_min,year_max))
            if '【来源国】' in q_template:  base_keyword_list=add_item(base_keyword_list, '来源国', from_country)
            if '【流向国】' in q_template:  base_keyword_list=add_item(base_keyword_list, '流向国', to_country)
            if '【领域】' in q_template:  base_keyword_list=add_item(base_keyword_list, '领域', field)
            if '【子领域】' in q_template:  base_keyword_list=add_item(base_keyword_list, '子领域', sub_field)
            if '【申请人】' in q_template:  base_keyword_list=add_item(base_keyword_list, '申请人', applicant)
            if '【发明人】' in q_template:  base_keyword_list=add_item(base_keyword_list, '发明人', inventor)
            if '【topN数目】' in q_template:  base_keyword_list=add_item(base_keyword_list, 'topN数目', range(top_min,top_max))
            for item in base_keyword_list:
                question=fill_base_key(q_template, item)
                print(question)

                for a_template in a_template_list:
                    answer=fill_base_key(a_template, item)
                    answer=fill_compute_key(answer,item)
                    set_sql(item)



def init():
    # 连接数据库
    link_database()

    # 读取国别编码的索引字典
    f = open('country_code.txt', mode='r', encoding='utf8')
    global code_dir
    for line in f.readlines():
        code_dir[line.split('\t')[0]] = line.split('\t')[1].replace('\r','').replace('\n','')


init()
main_deal()
db_conn.close()
# link_database()
# print(select("SELECT * FROM ana_des_20171121 LIMIT 10"))
