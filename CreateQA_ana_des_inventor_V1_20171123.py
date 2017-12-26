#-*-coding:utf-8-*-

# author: 景然
# data: 2017/11/21
# function: “发明人”问答知识生成
# input: MySQL[114.115.149.84],db[ANA_DES_20171121]
# output: 发明人问答QA知识，存入“问题.txt”

import MySQLdb as mdb
import re

f = open('问题.txt','w')

year = [2014, 2015, 2016]
country = ['中国', '美国', '日本']
scholar = ['周明杰', '陈庆', '戴加龙']
organization = ['东华大学', '中南大学', '浙江大学']

domain = ['机器学习', '语音识别']


config = {
        'host': '114.115.149.84',
        'port': 3306,
        'user': 'llc',
        'passwd': 'llc@patent123',
        'db': 'ANA_DES_20171121',
}

conn = mdb.connect(**config)

conn.set_character_set('utf8')

cursor = conn.cursor()

# 31
f.writelines('31.'+ 'XX年某人在XX领域的专利申请量是多少？'+"\n")
for s in scholar:
    for y in year:
        for d in domain:

            sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 申请年='%s' and 领域='%s'" %(s, y, d)
            # print sql
            cursor.execute(sql)
            result = cursor.fetchall()

            num = result[0][0]
            f.writelines("%s年，%s在%s领域的专利申请量为%s篇"%(y,s,d,num)+ "\n")

# 32
f.writelines('32.' +"\n")
for s in scholar:
    for y in year:
        for d in domain:
            for c in country:
                sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 申请年='%s' and 领域='%s' and 申请人国别代码='%s'"%(s,y,d,c)
                cursor.execute(sql)
                result = cursor.fetchall()

                num = result[0][0]
                f.writelines("%s年，%s在%s领域的%s专利申请量为%s篇" % (y, s, d, c, num)+ "\n")


f.writelines('33.'+ "\n")
for s in scholar:
    for y in year:
        for d in domain:
            sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 授权年='%s' and 领域='%s'" %(s, y, d)
            cursor.execute(sql)
            result = cursor.fetchall()

            num = result[0][0]
            f.writelines("%s年，%s在%s领域的专利授权量为%s篇" % (y, s, d, num)+ "\n")

# 34
f.writelines('35.'+ "\n")
for s in scholar:
    for y in year:
        for d in domain:
            for o in organization:
                sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 申请年='%s' and 领域='%s' and 申请人 like '%s'" % (s, y, d, o)
                cursor.execute(sql)
                result = cursor.fetchall()

                num = result[0][0]
                f.writelines("%s年，%s的%s在%s领域的专利申请量为%s篇" % (y, o, s, d, num)+ "\n")


f.writelines('36.'+ '在XX领域中，某人哪年的专利申请量最多？'+"\n")
for s in scholar:
    for d in domain:
        sql = "select 申请年, count(distinct 申请号) as num from ana_des_20171121_1 where 发明人='%s' and 领域='%s' GROUP BY 申请年 order by num desc limit 1;"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (s, d)+ "\n")
        else:
            topyear = result[0][0]
            f.writelines("%s在%s领域专利申请量最多的年份是%s年" % (s, d, topyear)+ "\n")


f.writelines('37.'+'某人在XX领域最新的专利是什么？'+ "\n")
for s in scholar:
    for d in domain:
        sql = "SELECT 标题 from ana_des_20171121_1 where 发明人 like '%s' and 领域='%s' ORDER BY 申请日 desc limit 1;"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (s, d)+ "\n")
        else:
            title = result[0][0]
            f.writelines("%s在%s领域最新申请的专利是'%s'" % (s, d, title)+ "\n")

f.writelines('38.'+ "\n")
for s in scholar:
    for d in domain:
        sql = "SELECT 标题 from ana_des_20171121_1 where 发明人 like '%s' and 领域='%s' ORDER BY 申请日 limit 1;"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (s, d)+ "\n")
        else:
            title = result[0][0]
            f.writelines("%s在%s领域最早申请的专利是'%s'" % (s, d, title)+ "\n")

f.writelines('40.'+ "\n")
for s in scholar:
    for d in domain:
        sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 领域='%s' and 专利有效性='有效';"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        num = result[0][0]
        f.writelines("%s在%s领域的有效专利数量为%s篇"%(s, d, num)+ "\n")

f.writelines('41.'+ "\n")
for s in scholar:
    for d in domain:
        sql = "select count(distinct 申请号) from ana_des_20171121_1 where 发明人 like '%s' and 领域='%s' and 简单同族 REGEXP 'JP|US|CN';"%(s, d)
        cursor.execute(sql)
        result = cursor.fetchall()

        num = result[0][0]
        f.writelines("%s在%s领域的三方专利数量为%s篇" % (s, d, num)+ "\n")


f.writelines('43.'+ "\n")
for s in scholar:
    for d in domain:
        sql = "select 标题 from ana_des_20171121_1 where 发明人='%s' and 领域='%s' order by 被引证次数 desc limit 1;"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (s, d)+ "\n")
        else:
            title = result[0][0]
            f.writelines("%s在%s领域的top1高被引专利是'%s'" % (s, d, title)+ "\n")

f.writelines('44.'+ '某人在XX领域的主要研究方向是什么？'+"\n")
for s in scholar:
    for d in domain:
        sql = "select 子领域, count(distinct 申请号) as num from ana_des_20171121_1 where 发明人='%s' and 领域='%s' GROUP BY 子领域 order by num desc limit 10;"%(s,d)
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (s, d)+ "\n")
        else:
            subdomain = []
            for i in result:
                sd = i[0]
                subdomain.append(sd)
            text = '、'.join(subdomain)
            f.writelines("%s在%s领域的主要研究方向是%s" % (s, d, text)+ "\n")