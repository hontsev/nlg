# -*- coding: UTF-8 -*-
# author: zhangyao
# data: 2017/12/27
# function: 问答生成主入口程序
# input:
# output:

import pymysql
import json
import datetime

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
        if len(ditem['公开（公告）日'])>0:num+=1
    return str(num)

def get_key13(item,data):
    num = 0
    for ditem in data:
        if ditem['专利有效性']=='有效' :num+=1
    return str(num)

def get_key14(item,data):
    num = 0
    for ditem in data:
        country=ditem['同族国家']
        if 'CN' in country and 'US' in country and 'JP' in country:
            num+=1
    return str(num)

def order_by_year(data):
    years = {}
    for ditem in data:
        # print(ditem)
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
        tcountry = ditem['申请人国别代码'].split(', ')
        for tc in tcountry:
            if tc not in country:
                country[tc] = 0
            country[tc] += 1
    # country.sort()
    result = sorted(country.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_othercountry(data,country):
    countries = {}
    for ditem in data:
        tcountry = ditem['申请人国别代码'].split(', ')
        for tc in tcountry:
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
        tpersons = ditem['申请人'].split('; ')
        for tp in tpersons:
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_otherperson(data,person):
    persons = {}
    for ditem in data:
        tpersons = ditem['申请人'].split('; ')
        for tp in tpersons:
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
        tpersons = ditem['申请人'].split('; ')
        for tp in tpersons:
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += int(ditem['家族被引证次数'])
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_subfield(data):
    subfields={}
    for ditem in data:
        subfield = str(ditem['子领域'])
        if subfield not in subfields:
            subfields[subfield] = 0
        subfields[subfield] += 1
    result=sorted(subfields.items(),key=lambda item:item[1],reverse=True)
    return result

def order_by_inventor(data):
    persons = {}
    for ditem in data:
        tpersons = ditem['发明人'].split('; ')
        for tp in tpersons:
            if tp not in persons:
                persons[tp] = 0
            persons[tp] += 1
    result = sorted(persons.items(), key=lambda item: item[1], reverse=True)
    return result

def order_by_otherinventor(data,inventor):
    persons = {}
    for ditem in data:
        tpersons = ditem['发明人'].split('; ')
        for tp in tpersons:
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
        print(persons)
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
        print(names)
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
        if len(ditem['申请日'])<=0:
            continue
        ttime=datetime.datetime.strptime(ditem['申请日'],'%Y/%m/%d')
        if ttime>lasttime:
            lasttime=ttime
            lastname=ditem['标题']
    return lastname

def get_key22(item,data):
    earlytime=datetime.datetime.strptime('9999/1/1','%Y/%m/%d')
    earlyname=''
    for ditem in data:
        if len(ditem['申请日'])<=0:
            continue
        ttime=datetime.datetime.strptime(ditem['申请日'],'%Y/%m/%d')
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
        persons=order_by_inventor(data,person)
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

def main_deal():
    qa_type_min=1
    qa_type_max=44 # 44

    year_min=2014
    year_max=2017
    top_min=1
    top_max=5
    # base_keyword={"【优先权年】"=}

    # 获取来源国字段的可能的取值
    from_country_tmp = select("SELECT distinct 申请人国别代码 FROM %s" % db_patent)
    from_country = list()
    for item in from_country_tmp:
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
    sub_field = list()
    sub_field_tmp = select("SELECT distinct 子领域 FROM %s" % db_patent)
    for item in sub_field_tmp: sub_field.append(item["子领域"])
    sub_field=sub_field#[0:5]

    # 申请人的可能取值
    applicant_tmp = select("SELECT distinct 申请人 FROM %s" % db_patent)
    applicant = list()
    for item in applicant_tmp:
        for name in item['申请人'].split(';'):
            if len(name.strip()) > 0:
                applicant.append(name.strip())
    applicant = list(set(applicant))[0:100]

    # 发明人的可能取值
    inventor_tmp = select("SELECT distinct 发明人 FROM %s" % db_patent)
    inventor = list()
    for item in inventor_tmp:
        for name in item['发明人'].split(';'):
            if len(name.strip()) > 0:
                inventor.append(name.strip())
    inventor = list(set(inventor))[0:100]

    result=list()

    
    for qa_type in range(qa_type_min, qa_type_max+1):
        q_template_list= select("SELECT content FROM q_template WHERE `type`='%s'" % qa_type)
        a_template_list = select("SELECT content FROM a_template WHERE `type`='%s'" % qa_type)
        # if len(q_template_list)<=0 or len(a_template_list)<=0:
            # continue
        # q_template_list=[{'content':'【优先权年】【授权年】【申请年】【来源国】【流向国】【领域】【子领域】【申请人】【发明人】【topN数目】'}]
        # q_template_list = [{'content': '在【优先权年】，申请年为【申请年】的，从【来源国】向【流向国】的，在【领域】领域的【子领域】子领域中的，由【申请人】申请，并且发明人为【发明人】的专利有哪些？'}]
        for q_template in q_template_list:
            q_template=q_template['content']
            base_keyword_list=[{"type":qa_type}]
            # sql="SELECT * FROM ana_des_20171121 "
            # is_first_condition=True;
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
            print(base_keyword_list.__len__())
            for item in base_keyword_list:
                # 填充问句
                question=fill_base_key(q_template, item)

                # print(question)

                for a_template in a_template_list:
                    a_template=a_template['content']

                    # 部分填充答句
                    answer=fill_base_key(a_template, item)

                    # 构建查询语句
                    sql=set_sql(item)
                    # sql="SELECT * FROM ana_des_20171121 WHERE `领域`='机器学习' limit 100"

                    # 从数据库得到计算所需数据
                    sqldata=select(sql)

                    # 按申请码去重
                    data_result=get_distinct( sqldata )
                    # break

                    # 填充答句的需计算部分
                    answer = fill_compute_key(answer, item,data_result)

                    result.append((question,answer))
                    # print(answer)
                # break
            #break

    output(result)

def output(data):
    f=open('output.txt',mode='w',encoding='utf-8')
    for item in data:
        f.write(item[0]+"\t"+item[1]+"\r\n")
    f.close()

def init():
    # 连接数据库
    link_database()

    # 读取国别编码的索引字典
    f = open('country_code.txt', mode='r', encoding='utf8')
    global code_dir
    for line in f.readlines():
        code_dir[line.split('\t')[0]] = line.split('\t')[1].replace('\r','').replace('\n','')

def update_templates():


    qf=open("question_template.txt",mode='r',encoding='utf8')
    question_templates=list()
    for line in qf.readlines():
        question_templates.append({ 'type' : line.split('\t')[0], 'content' : line.split('\t')[1].replace('\r','').replace('\n','')})
    execute("TRUNCATE q_template")
    for item in question_templates:
        execute("INSERT INTO q_template(content,type) VALUES('%s','%s')" %(item['content'],item['type']))


    af=open("answer_template.txt",mode='r',encoding='utf8')
    answer_templates=list()
    for line in af.readlines():
        answer_templates.append({ 'type' : line.split('\t')[0], 'content' : line.split('\t')[1].replace('\r','').replace('\n','')})
    execute("TRUNCATE a_template")
    for item in answer_templates:
        execute("INSERT INTO a_template(content,type) VALUES('%s','%s')" %(item['content'],item['type']))

init()
# update_templates()
main_deal()
db_conn.close()