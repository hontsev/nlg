# -*- coding: UTF-8 -*-
# author: zhangyao
# data: 2017/12/27
# function: 问答生成主入口程序
# input:
# output:

import pymysql
import json
import datetime
import time
import copy
import os

import re

dict_path='dict/'
key_cmp_file='qtype_to_akeytype.txt'
country_list='country_list.txt'
person_list='person_list.txt'
field_list='field_list.txt'
template_q_list='template_q_list.txt'
template_a_list='template_a_list.txt'
country_code="country_code.txt"

data_path='data/'
qa_pair_list='qa_pair_list.txt'
ka_pair_list='ka_pair_list.txt'


db_config_file = "db_config"
db_conn = object()

#db_patent='ana_des_20171121'

db_patent='ana_des_ai'
db_output='ana_des_result_20180301'
db_template_q='q_template'
db_template_a='a_template'

code_dir = dict()
key_cmp_dir = dict()

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
        print("select" + sql)
        start = time.clock()

        with db_conn.cursor() as cursor:
            # 执行sql语句，插入记录
            cursor.execute(sql)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            res = cursor.fetchall()
            db_conn.commit()
        end = time.clock()
        print("read: %f s" % (end - start))
        print("select over")
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

def safe_sql(data):
    # 单引号转码
    return data.replace('\'','\'\'')

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
        sql += "(`专利类型`='发明授权'or`专利类型`='实用新型'or`专利类型`='外观设计') and SUBSTR(`公开（公告）日`,1,4)='%s'" % item['授权年']
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
               (safe_sql(item['申请人']),safe_sql(item['申请人']),safe_sql(item['申请人']),safe_sql(item['申请人']))
    if '发明人' in item:
        if is_first_condition:
            is_first_condition = False
            sql += " WHERE "
        else:
            sql += " AND "
        sql += "(`发明人`='%s' or `发明人` REGEXP '^%s[;]+' or `发明人` REGEXP '[;[:space:]]+%s$' or `发明人` REGEXP '[;[:space:]]+%s[;]+')" % \
               (safe_sql(item['发明人']), safe_sql(item['发明人']), safe_sql(item['发明人']), safe_sql(item['发明人']))
    # print(sql)
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

def get_key11(item,data):
    return str(len(data))

def get_key12(item,data):
    num=0
    for ditem in data:
        if len(str(ditem['公开（公告）日']))>0:num+=1
    return str(num)

def get_key13(item,data):
    num = 0
    for ditem in data:
        if str(ditem['专利有效性'])=='有效' :num+=1
    return str(num)

def get_key14(item,data):
    num = 0
    for ditem in data:
        country=str(ditem['同族国家'])
        if 'CN' in country and 'US' in country and 'JP' in country:
            num+=1
    return str(num)

def order_by_year(data):
    years = {}
    for ditem in data:
        # print(ditem)
        if ditem['申请日'] == None: continue
        thisyear = str(ditem['申请日'])[0:4]
        if len(thisyear)<=0:
            continue
        if thisyear not in years:
            years[thisyear] = 0
        years[thisyear] += 1
    result=sorted(years.items(),key=lambda item:item[1],reverse=True)
    return result

def order_by_country(data):
    country = {}
    for ditem in data:
        if ditem['申请人国别代码'] == None:continue
        tcountry = ditem['申请人国别代码'].split(',')
        for tc in tcountry:
            tc = tc.strip()
            if tc not in country:
                country[tc] = 0
            country[tc] += 1
    # country.sort()
    result = sorted(country.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_othercountry(data,country):
    countries = {}
    for ditem in data:
        if ditem['申请人国别代码'] == None: continue
        tcountry = ditem['申请人国别代码'].split(',')
        for tc in tcountry:
            tc = tc.strip()
            if (tc == country) or (country not in tcountry):
                continue
            if tc not in countries:
                countries[tc] = 0
            countries[tc] += 1
    result = sorted(countries.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_person(data):
    persons = {}
    for ditem in data:
        if ditem['申请人'] == None: continue
        tpersons = ditem['申请人'].split(';')
        for tp in tpersons:
            tp = tp.strip()
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_otherperson(data,person):
    persons = {}
    for ditem in data:
        if ditem['申请人'] == None: continue
        tpersons = ditem['申请人'].split(';')
        for tp in tpersons:
            tp = tp.strip()
            if (tp == person) or (person not in tpersons):
                continue
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_gperson(data):
    persons = {}
    for ditem in data:
        if ditem['申请人'] == None: continue
        tpersons = ditem['申请人'].split(';')
        for tp in tpersons:
            tp = tp.strip()
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += int(ditem['家族被引证次数'])
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_subfield(data):
    subfields={}
    for ditem in data:
        if ditem['子领域'] == None: continue
        tsubfields = ditem['子领域'].split(';')
        for sf in tsubfields:
            sf = sf.strip()
            if sf not in subfields:
                subfields[sf]=0
            subfields[sf]+=1
    result=sorted(subfields.items(),key=lambda item:item[1],reverse=True)
    return result

def order_by_inventor(data):
    persons = {}
    for ditem in data:
        if ditem['发明人'] == None: continue
        tpersons = ditem['发明人'].split('; ')
        for tp in tpersons:
            tp = tp.strip()
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_otherinventor(data,inventor):
    persons = {}
    for ditem in data:
        if ditem['发明人'] == None: continue
        tpersons = ditem['发明人'].split(';')
        for tp in tpersons:
            tp = tp.strip()
            if (tp == inventor) or (inventor not in tpersons):
                continue
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result


def order_by_person_type(data):
    ptypes = {}
    for ditem in data:
        if ditem['申请人类型'] == None: continue
        ttype = ditem['申请人类型']
        if len(ttype)<=0:
            continue
        if ttype not in ptypes:
            ptypes[ttype] = 0
        ptypes[ttype] += 1
    result = sorted(ptypes.items(), key=lambda item: item[1], reverse=True)
    return result


def get_key15(item,data):
    years=order_by_year(data)
    if len(years)<=0:
        return ''
    return years[0][0]

def get_key16(item,data):
    tmpyears=order_by_year(data)
    years={}
    for y in tmpyears:
        years[y[0]]=y[1]
    maxyear=0
    maxdata=0
    for year in years:
        if str(int(year)-1) in years:
            # 有前一年的数据才能算
            tdata=years[year]-years[str(int(year)-1)]
            if tdata > maxdata:
                maxdata=tdata
                maxyear=year
    return str(maxyear)

def get_key17(item,data):
    if 'topN数目' in item:
        topn=int(item['topN数目'])
        countries=order_by_country(data)
        result=""
        topn=min(topn,len(countries))
        for i in range(0,topn):
            if i>0:
                if i==topn-1:
                    result+="和"
                else:
                    result+="、"
            result+=str(countries[i][0])
        return result
    else :
        return ''

def get_key18(item,data):
    if 'topN数目' in item:
        topn=int(item['topN数目'])
        persons=order_by_person(data)
        result=""
        topn=min(topn,len(persons))
        for i in range(0,topn):
            if i>0:
                result+="、"
            result+=str(persons[i][0])
        return result
    else :
        return ''

def get_key19(item,data):
    if 'topN数目' in item:
        topn=int(item['topN数目'])
        persons=order_by_gperson(data)
        result=""
        # print(persons)
        topn=min(topn,len(persons))
        for i in range(0,topn):
            if i>0:
                result+="、"
            result+=str(persons[i][0])
        return result
    else :
        return ''

def get_key20(item,data):
    if 'topN数目' in item:
        topn=int(item['topN数目'])
        names=[]
        for ditem in data:
            names.append((ditem['标题'],ditem['家族被引证次数']))
        names=sorted(names,key=lambda item:item[1],reverse=True)
        topn=min(topn,len(names))
        result=''
        # print(names)
        for i in range(0,topn):
            if i>0:
                result+="、"
            result+=str(names[i][0])
        return result
    else :
        return ''

def get_key21(item,data):
    lasttime=datetime.datetime.strptime('0001/1/1','%Y/%m/%d')
    lastname=''
    for ditem in data:
        if ditem['申请日'] == None: continue
        if len(str(ditem['申请日']))<=0:
            continue
        # ttime=datetime.datetime.strptime(str(ditem['申请日']),'%Y/%m/%d')
        ttime=ditem['申请日']
        if ttime>lasttime:
            lasttime=ttime
            lastname=ditem['标题']
    return lastname

def get_key22(item,data):
    earlytime=datetime.datetime.strptime('9999/1/1','%Y/%m/%d')
    earlyname=''
    for ditem in data:
        if ditem['申请日'] == None: continue
        if len(str(ditem['申请日']))<=0:
            continue
        # ttime=datetime.datetime.strptime(str(ditem['申请日']),'%Y/%m/%d')
        ttime = ditem['申请日']
        if ttime<earlytime:
            earlytime=ttime
            earlyname=ditem['标题']
    return earlyname

def get_key23(item,data):
    return ''

def get_key24(item,data):
    subfields=order_by_subfield(data)
    if len(subfields)<=0:
        return ''
    return subfields[0][0]

def get_key25(item,data):
    if '申请人' in item:
        person=item['申请人']
        persons=order_by_otherperson(data,person)
        if len(persons)<=0:
            return ''
        return persons[0][0]
    else:
        return ''

def get_key26(item,data):
    if '发明人' in item:
        person=item['发明人']
        persons=order_by_otherinventor(data,person)
        if len(persons)<=0:
            return ''
        return persons[0][0]
    else:
        return ''

def get_key27(item,data):
    person_types=order_by_person_type(data)
    if len(person_types)<=0:
        return ''
    return person_types[0][0]

def get_key28(item,data):
    if '来源国' in item:
        country=item['来源国']
        countries=order_by_othercountry(data,country)
        if len(countries)<=0:
            return ''
        return countries[0][0]
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

def fill_compute_key(template, item, data):
    result = template
    result = result.replace('【专利申请量】', get_key11(item,data))
    result = result.replace('【专利授权量】', get_key12(item, data))
    result = result.replace('【有效专利量】', get_key13(item, data))
    result = result.replace('【三方专利量】', get_key14(item, data))
    result = result.replace('【专利申请量最多的年份】', get_key15(item, data))
    result = result.replace('【专利申请量增长最快的年份】', get_key16(item, data))
    result = result.replace('【专利申请量topN的来源国】', get_key17(item, data))
    result = result.replace('【专利申请量topN的申请人】', get_key18(item, data))
    result = result.replace('【专利族高被引topN的申请人】', get_key19(item, data))
    result = result.replace('【专利族高被引topN的专利名称】', get_key20(item, data))
    result = result.replace('【最新申请的专利名称】', get_key21(item, data))
    result = result.replace('【最早申请的专利名称】', get_key22(item, data))
    result = result.replace('【专利申请趋势】', get_key23(item, data))
    result = result.replace('【主要研究方向】', get_key24(item, data))
    result = result.replace('【与申请人合作最多的申请人】', get_key25(item, data))
    result = result.replace('【与发明人合作最多的发明人】', get_key26(item, data))
    result = result.replace('【最多申请人类型】', get_key27(item, data))
    result = result.replace('【与来源国合作最多的来源国】', get_key28(item, data))
    # item['topN数目']=3
    # item['申请人']='山东玉皇化工有限公司'
    # item['发明人'] = '刘家伟'
    # item['来源国'] = '美国'
    # print(get_key28(item,data))
    # print(order_by_country(data))
    return result

def get_compute_key_single(item,data,type):
    return globals().get("get_key%s"% key_cmp_dir[str(type)])(item,data)




# 按专利的去重规则，过滤重复的专利项
def get_distinct(data):
    result=dict()
    for item in data:
        code1 = item['公开（公告）号'][0:-1]
        code2 = item['公开（公告）号'][-1:]
        # 最后一位是数字，就取倒数第二位作为标识位
        if code2.isdigit():
            code1 = item['公开（公告）号'][0:-2]
            code2 = item['公开（公告）号'][-2:-1]
            # print(code1)
            # print(code2)
            # print(item['公开（公告）号'])
        if item['专利类型'][0:2]=='发明':
            if code1 in result:
                if code2=='B' or code2=='C':
                    # 用B或C类型来替换原有类型
                    result[code1]={code2:item}
                    break
            else:
                # 初始化
                result[code1]={code2:item}
        else:
            result[code1] = {code2: item}
    # print(len(data))
    resultlist=list()
    for item in result.values():
        resultlist.append((item.popitem())[1])
    return resultlist

def add_prepare_data(dir,indexs,key,item):
    for i in indexs:
        if key in dir[i]:
            dir[i][key].append(item)
        else:
            dir[i][key] = [item]
    # return dir





def main_deal2():
    print("start")

    # 问答种类取值
    # qa_type_min=1
    # qa_type_max=44 # 44

    # topN取值
    top_n=range(1,5)

    alldata=select("SELECT * FROM %s" % db_patent)

    print("select end")

    # prepare_data=dict()
    for type in range(1,45):
        q_template_list=get_question_templates(type)
        a_template_list=get_answer_templates(type)
        print(q_template_list)

        # 为了得到这个类型对应的那些key
        template_classic=q_template_list[0]['content']

        # prepare_data[type]=dict()
        data=dict()

        for item in alldata:
            keys=dict()

            if item['优先权信息'] is None: keys['优先权年']=[item['申请日'].year]
            else : keys['优先权年']=[item['优先权信息'].split(' ')[0][-4:]]

            if item['授权公告日'] is None:keys['授权年'] = [item['申请日'].year]
            else: keys['授权年'] = [item['授权公告日'].year]

            keys['申请年']=[item['申请日'].year]

            if item['申请人国别代码'] is None: keys['来源国'] = [""]
            else: keys['来源国']=item['申请人国别代码'].split(',')

            keys['流向国']=[ code_dir[item['公开（公告）号'][0:2]]]

            keys['领域']=[item['领域']]

            keys['子领域']=[item['子领域'].split(';')]

            if item['申请人'] is None: keys['申请人'] =item['发明人'].split(';')
            else: keys['申请人']=item['申请人'].split(';')

            if item['发明人'] is None: keys['发明人'] = item['申请人'].split(';')
            else: keys['发明人']=item['发明人'].split(';')

            keys['topN数目']=[1,2,3,4,5]

            this_items=[{'type':type}]
            for keyname in keys:
                if "【%s】" % keyname in template_classic:
                    # print(keyname)
                    tmp_items=list()
                    for i1 in this_items:
                        for i2 in keys[keyname]:
                            # print("%s,%s" % (i1,i2))
                            tmp=copy.deepcopy(i1)
                            tmp[keyname]=str(i2).strip()
                            tmp_items.append(tmp)
                            # i1[keyname]=str(i2).strip()
                    this_items=tmp_items
            # print(this_items)
            # return

            for sub_item in this_items:
                key = ""
                for part in sub_item:
                    key+="%s:%s|" % (part,sub_item[part])
                if key in data:
                    data[key].append(item)
                else:
                    data[key]=[item]

        result=list()
        result_index=list()
        for key in data:
            item={}
            tmp1=key.split('|')
            for part in tmp1:
                if(len(part)<=0): continue
                k,v=part.split(':',1)
                item[k]=v

            for q_template in q_template_list:
                q_template=q_template['content']
                q = fill_question(q_template,item)

                # print(q)
                for a_template in a_template_list:
                    a_template=a_template['content']
                    a = fill_answer_with_data(a_template,item,data[key])
                    answer_single=get_compute_key_single(item,data[key],type)
                    if '优先权年' not in item: item['优先权年']=''
                    if '授权年' not in item: item['授权年'] = ''
                    if '申请年' not in item: item['申请年'] = ''
                    if '来源国' not in item: item['来源国'] = ''
                    if '流向国' not in item: item['流向国'] = ''
                    if '领域' not in item: item['领域'] = ''
                    if '子领域' not in item: item['子领域'] = ''
                    if '申请人' not in item: item['申请人'] = ''
                    if '发明人' not in item: item['发明人'] = ''
                    if 'topN数目' not in item: item['topN数目'] = ''
                    result_index.append((type,item['优先权年'],item['授权年'],item['申请年'],item['来源国'],item['流向国'],item['领域'],item['子领域'],item['申请人'],item['发明人'],item['topN数目'],answer_single))
                    # print(a)

                    result.append((q, a))

                    # execute("INSERT INTO %s(id,question,answer,author) VALUES('%s','%s','%s','%s')" % (
                    # db_output, type, safe_sql(q), safe_sql(a), '张尧'))
        print("%s finish" % type)
        output_txt2(result_index,type)
        output_txt(result,type)


def main_deal():

    print("开始获取可能的取值…")

    # 问答种类取值
    qa_type_min=1
    qa_type_max=44 # 44

    # 年份取值
    year_min=2000
    year_max=2017

    # topN取值
    top_min=1
    top_max=5
    # base_keyword={"【优先权年】"=}

    # 获取来源国字段的可能的取值
    from_country_tmp = select("SELECT distinct 申请人国别代码 FROM %s" % db_patent)
    from_country = list()
    for item in from_country_tmp:
        # print(item['申请人国别代码'])
        if item['申请人国别代码']==None:continue
        for country in item['申请人国别代码'].split(','):
            if len(country.strip()) > 0:
                from_country.append(country.strip())
    from_country = list(set(from_country))#[0:5]

    # 获取流向国的可能取值，这里是取得其英文字母编号
    to_country_tmp = select("SELECT distinct SUBSTRING(公开（公告）号,1,2) as 流向国国别代码 FROM %s" % db_patent)
    to_country = list()
    for item in to_country_tmp: to_country.append(item['流向国国别代码'])
    to_country = list(set(to_country))#[0:5]

    # 领域的可能取值
    field=list()
    field_tmp = select("SELECT distinct 领域 FROM %s" % db_patent)
    for item in field_tmp:field.append(item["领域"])
    field=field#[0:5]

    # 子领域的可能取值
    sub_field_tmp = select("SELECT distinct 子领域 FROM %s" % db_patent)
    # for item in sub_field_tmp: sub_field.append(item["子领域"])
    sub_field = list()
    for item in sub_field_tmp:
        if item['子领域'] == None: continue
        for name in item['子领域'].split(';'):
            if len(name.strip()) > 0:
                sub_field.append(name.strip())
    sub_field=sub_field#[0:5]

    # 申请人的可能取值
    applicant_tmp = select("SELECT distinct 申请人 FROM %s" % db_patent)
    applicant = list()
    for item in applicant_tmp:
        if item['申请人'] == None: continue
        for name in item['申请人'].split(';'):
            if len(name.strip()) > 0:
                applicant.append(name.strip())
    applicant = list(set(applicant))#[0:100]

    # 发明人的可能取值
    inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
    inventor = list()
    for item in inventor_tmp:
        if item['发明人'] == None: continue
        for name in item['发明人'].split(';'):
            if len(name.strip()) > 0:
                inventor.append(name.strip())
    inventor = list(set(inventor))#[0:100]


    # 输出当前配置
    print("发明信息数据库 %s 数据条数 %s" % (db_patent,select("SELECT count(*) AS 'count' FROM %s" % db_patent)[0]['count']))
    print("问答类型取值为 %s - %s" % (qa_type_min,qa_type_max))
    print("时间取值为 %s - %s" % (year_min, year_max))
    print("tonN个数取值为 %s - %s" % (top_min, top_max))
    print("来源国个数 %s" % len(from_country))
    print("流向国个数 %s" % len(to_country))
    print("领域个数 %s" % len(field))
    print("子领域个数 %s" % len(sub_field))
    print("申请人个数 %s" % len(applicant))
    print("发明人个数 %s" % len(inventor))

    # return

    num=0
    for qa_type in range(qa_type_min, qa_type_max+1):
        if qa_type == 35 or qa_type == 33 or qa_type == 32 or qa_type == 31:
            continue
        result = list()
        q_template_list= get_question_templates(qa_type)
        a_template_list = get_answer_templates(qa_type)
        # if len(q_template_list)<=0 or len(a_template_list)<=0:
            # continue
        # q_template_list=[{'content':'【优先权年】【授权年】【申请年】【来源国】【流向国】【领域】【子领域】【申请人】【发明人】【topN数目】'}]
        # q_template_list = [{'content': '在【优先权年】，申请年为【申请年】的，从【来源国】向【流向国】的，在【领域】领域的【子领域】子领域中的，由【申请人】申请，并且发明人为【发明人】的专利有哪些？'}]
        print("类型%s有%s个问题模板和%s个答案模板" % (qa_type,len(q_template_list),len(a_template_list)))
        for q_template in q_template_list:
            q_template=q_template['content']
            base_keyword_list=[{"type":qa_type}]
            # sql="SELECT * FROM ana_des_20171121 "
            # is_first_condition=True;

            item_num=1
            if '【优先权年】' in q_template: item_num *= len(range(year_min,year_max+1))
            if '【授权年】' in q_template: item_num *= len(range(year_min,year_max+1))
            if '【申请年】' in q_template:item_num *= len(range(year_min,year_max+1))
            if '【来源国】' in q_template:item_num *= len(from_country)
            if '【流向国】' in q_template:item_num *= len(to_country)
            if '【领域】' in q_template:item_num *= len(field)
            if '【子领域】' in q_template:item_num *= len(sub_field)
            if '【申请人】' in q_template:item_num *= len(applicant)
            if '【发明人】' in q_template:item_num *= len(inventor)
            if '【topN数目】' in q_template:item_num *= len(range(top_min,top_max+1))
            num += item_num * len(a_template_list)
            print("将产生%s个问答对，总计产生%s个。" % (item_num, num))
            # continue


            if '【优先权年】' in q_template:  base_keyword_list=add_item(base_keyword_list,'优先权年',range(year_min,year_max+1))
            if '【授权年】' in q_template:  base_keyword_list=add_item(base_keyword_list,'授权年',range(year_min,year_max+1))
            if '【申请年】' in q_template:  base_keyword_list=add_item(base_keyword_list, '申请年', range(year_min,year_max+1))
            if '【来源国】' in q_template:  base_keyword_list=add_item(base_keyword_list, '来源国', from_country)
            if '【流向国】' in q_template:  base_keyword_list=add_item(base_keyword_list, '流向国', to_country)
            if '【领域】' in q_template:  base_keyword_list=add_item(base_keyword_list, '领域', field)
            if '【子领域】' in q_template:  base_keyword_list=add_item(base_keyword_list, '子领域', sub_field)
            if '【申请人】' in q_template:  base_keyword_list=add_item(base_keyword_list, '申请人', applicant)
            if '【发明人】' in q_template:  base_keyword_list=add_item(base_keyword_list, '发明人', inventor)
            if '【topN数目】' in q_template:  base_keyword_list=add_item(base_keyword_list, 'topN数目', range(top_min,top_max+1))




            for item in base_keyword_list:
                # 填充问句
                question=fill_question(q_template, item)
                print(question)
                # print(question)

                for a_template in a_template_list:
                    a_template=a_template['content']

                    answer=fill_answer(a_template,item)

                    result.append((question,answer))

                    execute("INSERT INTO %s(id,question,answer,author) VALUES('%s','%s','%s','%s')" % (db_output, qa_type, safe_sql(question), safe_sql(answer), '张尧'))
                    # print(answer)
                # break
            #break

        output_txt(result,qa_type)

# 按照如下格式存入txt：类型-优先权年-授权年-申请年-来源国-流向国-领域-子领域-申请人-发明人-topN数目-答案
def output_txt2(data,typename):
    typename = str(typename)
    f = open(data_path+'ka_pair_%s.txt'% typename, mode='w', encoding='utf-8')
    for item in data:
        line=''
        for lineitem in item:
            line+='%s\t' % lineitem
        line+='\r'
        f.write(line)
    f.close()

# 按照问句-答句的形式存入文本文件
def output_txt(data,typename):
    typename = str(typename)
    f=open(data_path+'qa_pair_%s.txt'%typename,mode='w',encoding='utf-8')
    for item in data:
        f.write(item[0]+"\t"+item[1]+"\r")
    f.close()

def output_db(data,typename):
    typename = str(typename)
    print(typename + ',' + str(len(data)))
    for item in data:
        execute("INSERT INTO %s(id,question,answer,author) VALUES('%s','%s','%s','%s')" %(db_output,typename,safe_sql(item[0]),safe_sql(item[1]),'张尧'))

def init():
    # 连接数据库
    link_database()

    # dict
    if not os.path.exists(dict_path):os.makedirs(dict_path)
    if not os.path.exists(data_path):os.makedirs(data_path)

    # 读取国别编码的索引字典
    f = open(dict_path+country_code, mode='r', encoding='utf8')
    global code_dir
    for line in f.readlines():
        code_dir[line.split('\t')[0]] = line.split('\t')[1].replace('\r','').replace('\n','')

    # 读取问题-答案关键词id的对应字典
    f = open(dict_path+key_cmp_file,mode='r',encoding='utf-8')
    global key_cmp_dir
    for line in f.readlines():
        key_cmp_dir[line.split('\t')[0]]=line.split('\t')[1].replace('\r','').replace('\n','')


def update_templates():
    # 从问句、答句模板文件中更新数据库中的模板
    qf=open(dict_path+template_q_list,mode='r',encoding='utf8')
    question_templates=list()
    for line in qf.readlines():
        question_templates.append({ 'type' : line.split('\t')[0], 'content' : line.split('\t')[1].replace('\r','').replace('\n','')})
    execute("TRUNCATE %s" % (db_template_q))
    for item in question_templates:
        execute("INSERT INTO %s(content,type) VALUES('%s','%s')" %(db_template_q,item['content'],item['type']))


    af=open(dict_path+template_a_list,mode='r',encoding='utf8')
    answer_templates=list()
    for line in af.readlines():
        answer_templates.append({ 'type' : line.split('\t')[0], 'content' : line.split('\t')[1].replace('\r','').replace('\n','')})
    execute("TRUNCATE %s" %(db_template_a))
    for item in answer_templates:
        execute("INSERT INTO %s(content,type) VALUES('%s','%s')" %(db_template_a,item['content'],item['type']))

def get_question_templates(qa_type):
    return select("SELECT content FROM %s WHERE `type`='%s'" % (db_template_q, qa_type))

def get_answer_templates(qa_type):
    return select("SELECT content FROM %s WHERE `type`='%s'" % (db_template_a, qa_type))


def fill_question(q_template,item):
    question=fill_base_key(q_template, item)
    return question

def fill_answer_with_data(a_template,item,data):
    data_result = get_distinct(data)
    answer = fill_base_key(a_template, item)
    answer=fill_compute_key(answer, item,data_result)
    return answer

def fill_answer(a_template,item):
    # 部分填充答句
    answer = fill_base_key(a_template, item)
    # 构建查询语句
    sql = set_sql(item)
    # sql="SELECT * FROM ana_des_20171121 WHERE `领域`='机器学习' limit 100"

    # 从数据库得到计算所需数据
    sqldata = select(sql)

    # 按申请码去重
    data_result = get_distinct(sqldata)

    # 填充答句的需计算部分
    answer = fill_compute_key(answer, item, data_result)

    return answer

# 将生成的数据保存成同一个txt，便于导入数据库
def merge_all_output():
    # 问答句
    all_data=list()
    all_data.append("question\tanswer\r")
    for i in range(1,45):
        f = open(data_path+'qa_pair_%s.txt'% i , mode='r', encoding='utf-8')
        items=f.readlines()
        all_data+=items
        f.close()
    f = open(data_path+qa_pair_list, mode='w', encoding='utf-8')
    for line in all_data:
        if len(line.strip())>0:
            f.write(line)
    f.close()

    # 关键词-答案对
    all_data=list()
    all_data.append("type\ty1\ty2\ty3\tc1\tc2\ta1\ta2\tp1\tp2\ttopN\tres\t\r")
    for i in range(1,45):
        typename=str(i)
        f = open(data_path+'ka_pair_%s.txt' % i, mode='r', encoding='utf-8')
        items = f.readlines()
        all_data += items
        f.close()
    f = open(data_path+ka_pair_list, mode='w', encoding='utf-8')
    for line in all_data:
        if len(line.strip()) > 0:
            f.write(line)
    f.close()

def delete_old_output():
    print("删除旧生成数据")
    execute("DELETE FROM %s WHERE author='%s'" % (db_output,'张尧'))

# 导出国家列表、领域列表、人名组织名列表
def save_key_list():
    # 获取来源国字段的可能的取值
    from_country_tmp = select("SELECT distinct 申请人国别代码 FROM %s" % db_patent)
    from_country = list()
    for item in from_country_tmp:
        # print(item['申请人国别代码'])
        if item['申请人国别代码'] == None: continue
        for country in item['申请人国别代码'].split(','):
            if len(country.strip()) > 0:
                from_country.append(country.strip())
    from_country = list(set(from_country))  # [0:5]

    # 获取流向国的可能取值，这里是取得其英文字母编号
    to_country_tmp = select("SELECT distinct SUBSTRING(公开（公告）号,1,2) as 流向国国别代码 FROM %s" % db_patent)
    to_country = list()
    # 转化为中文国名
    for item in to_country_tmp: to_country.append(code_dir[item['流向国国别代码']])
    to_country = list(set(to_country))  # [0:5]

    countries=list()
    for item in from_country:
        if item not in countries:
            countries.append(item)
    for item in to_country:
        if item not in countries:
            countries.append(item)
    f=open(dict_path+country_list,mode='w',encoding='utf-8')
    for item in countries:
        f.write(item+"\r")
    # f.writelines(countries)
    f.close()

    # 领域的可能取值
    field = dict()
    field_tmp = select("SELECT distinct 领域,子领域 FROM %s" % db_patent)
    for item in field_tmp:
        fname=item["领域"].strip()
        for sname in item['子领域'].split(';'):
            sname=sname.strip()
            if len(sname) > 0:
                keyname=fname+"\t"+sname
                field[keyname]=1
    f=open(dict_path+field_list,mode='w',encoding='utf-8')
    for item in field.keys():
        f.write(item+"\r")
    f.close()

    # 申请人的可能取值
    applicant_tmp = select("SELECT distinct 申请人 FROM %s" % db_patent)
    applicant = list()
    for item in applicant_tmp:
        if item['申请人'] == None: continue
        for name in item['申请人'].split(';'):
            if len(name.strip()) > 0:
                applicant.append(name.strip())
    applicant = list(set(applicant))  # [0:100]

    # 发明人的可能取值
    inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
    inventor = list()
    for item in inventor_tmp:
        if item['发明人'] == None: continue
        for name in item['发明人'].split(';'):
            if len(name.strip()) > 0:
                inventor.append(name.strip())
    inventor = list(set(inventor))  # [0:100]

    person=list()
    for item in applicant:
        if item not in countries:
            person.append(item)
    for item in inventor:
        if item not in countries:
            person.append(item)
    f=open(dict_path+person_list,mode='w',encoding='utf-8')
    for item in person:
        f.write(item+"\r")
    # f.writelines(countries)
    f.close()


# 得到ner格式的语料文件
def output_ner_corpus():
    f=open(data_path+ka_pair_list,encoding="utf-8",mode="r")
    lines=f.readlines()
    qt=dict()
    at=dict()
    reslist = list()
    for i in range(1,45):
        qt[str(i)]=get_question_templates(i)
        at[str(i)]=get_answer_templates(i)
    df=True
    for line in lines:
        # print(line.strip().split("\t"))
        if df or len(line.strip().split("\t"))!=12:
            df=False
            continue
        #print(line,len(line.strip().split("\t")))
        for type,y1,y2,y3,c1,c2,a1,a2,p1,p2,topN,res in [line.strip().split("\t")]:
            ql=qt[type]
            al=at[type]
            for q in ql:
                for a in al:
                    q=q["content"]
                    a=a["content"]
                    if len(y1) > 0: q = q.replace('【申请年】', "{{time:%s}}"%y1).replace('【授权年】', "{{time:%s}}"%y1).replace('【优先权年】', "{{time:%s}}"%y1); a = a.replace('【申请年】', "{{time:%s}}"%y1).replace('【授权年】', "{{time:%s}}"%y1).replace('【优先权年】', "{{time:%s}}"%y1)
                    if len(y2) > 0: q = q.replace('【申请年】', "{{time:%s}}"%y2).replace('【授权年】', "{{time:%s}}"%y2).replace('【优先权年】', "{{time:%s}}"%y2);a = a.replace('【申请年】', "{{time:%s}}"%y2).replace('【授权年】', "{{time:%s}}"%y2).replace('【优先权年】', "{{time:%s}}"%y2)
                    if len(y3) > 0: q = q.replace('【申请年】', "{{time:%s}}"%y3).replace('【授权年】', "{{time:%s}}"%y3).replace('【优先权年】', "{{time:%s}}"%y3);a = a.replace('【申请年】', "{{time:%s}}"%y3).replace('【授权年】', "{{time:%s}}"%y3).replace('【优先权年】', "{{time:%s}}"%y3)
                    if len(c1) > 0: q = q.replace('【来源国】', "{{location:%s}}" % c1);a = a.replace('【来源国】',"{{location:%s}}" % c1)
                    if len(c2) > 0: q = q.replace('【流向国】', "{{location:%s}}" % c2);a = a.replace('【流向国】',"{{location:%s}}" % c2)
                    if len(a1) > 0: q = q.replace('【领域】', "{{product_name:%s}}"%a1);a = a.replace('【领域】', "{{product_name:%s}}"%a1)
                    if len(a2) > 0: q = q.replace('【子领域】', "{{product_name:%s}}"%a2);a = a.replace('【子领域】', "{{product_name:%s}}"%a2)
                    if len(p1) > 0: q = q.replace('【申请人】', "{{person_name:%s}}"%p1);a = a.replace('【申请人】', "{{person_name:%s}}"%p1)
                    if len(p2) > 0: q = q.replace('【发明人】', "{{person_name:%s}}"%p2);a = a.replace('【发明人】', "{{person_name:%s}}"%p2)
                    if len(topN) > 0: q = q.replace('【topN数目】', topN);a = a.replace('【topN数目】', topN)
                    a = a.replace('【专利申请量】', res)
                    a = a.replace('【专利授权量】', res)
                    a = a.replace('【有效专利量】', res)
                    a = a.replace('【三方专利量】', res)
                    a = a.replace('【专利申请量最多的年份】', "{{time:%s}}"%res)
                    a = a.replace('【专利申请量增长最快的年份】', "{{time:%s}}"%res)
                    a = a.replace('【专利申请量topN的来源国】', "{{location:%s}}"%res)
                    a = a.replace('【专利申请量topN的申请人】', "{{person_name:%s}}"%res)
                    a = a.replace('【专利族高被引topN的申请人】', "{{person_name:%s}}"%res)
                    a = a.replace('【专利族高被引topN的专利名称】', res)
                    a = a.replace('【最新申请的专利名称】', res)
                    a = a.replace('【最早申请的专利名称】', res)
                    a = a.replace('【专利申请趋势】', res)
                    a = a.replace('【主要研究方向】', "{{product_name:%s}}"%res)
                    a = a.replace('【与申请人合作最多的申请人】', "{{person_name:%s}}"%res)
                    a = a.replace('【与发明人合作最多的发明人】', "{{person_name:%s}}"%res)
                    a = a.replace('【最多申请人类型】', res)
                    a = a.replace('【与来源国合作最多的来源国】', "{{location:%s}}"%res)
                    # print(q)
                    # print(a)
                    reslist.append("%s\r%s\r" % (q,a))

    f2=open(data_path+"corpus.txt",mode="w",encoding="utf-8")
    f2.writelines(reslist)



if __name__ == '__main__':
    init()
    # delete_old_output()
    # update_templates()
    # main_deal2()
    # merge_all_output()
    # save_key_list()
    # output_ner_corpus()
    db_conn.close()