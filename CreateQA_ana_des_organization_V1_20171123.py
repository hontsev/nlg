# -*- coding: UTF-8 -*-
# author: xiaoxiang
# data: 2017/12/24
# function: 机构问答模板生成
# input: MySQL[114.115.149.84],db[ANA_DES_20171121]
# output: QA_Organization.txt
import MySQLdb

database = MySQLdb.connect(host='114.115.149.84', user='llc', passwd='llc@patent123', db='ANA_DES_20171121')
database.set_character_set('utf8')
cur = database.cursor()

'''

"select count(distinct 申请号) from ana_des_20171121 where 申请日 like '%2016%' and 领域 like '机器学习' and 申请人 like '浙江大学';"
"select count(distinct 申请号) from ana_des_20171121 where 申请日 like '%2016%' and 领域 like '机器学习' and 子领域 like '深度学习' and 申请人 like '浙江大学';"

"select count(distinct 申请号) from ana_des_20171121 where 授权公告日 like '%2016%' and 领域 like '机器学习' and 申请人 like '浙江大学';"
"select count(distinct 申请号) from ana_des_20171121 where 授权公告日 like '%2016%' and 领域 like '机器学习' and 子领域 like '深度学习' and 申请人 like '浙江大学';"

"select count(distinct 申请号) from ana_des_20171121 where 申请日 like '%2016%' and 领域 like '机器学习' and 申请人 like '浙江大学' and 申请号 like '%US%';"
"select count(distinct 申请号) from ana_des_20171121 where 申请日 like '%2016%' and 领域 like '机器学习' and 子领域 like '深度学习' and 申请人 like '浙江大学' and 申请号 like '%US%';"

"select 申请人, count(distinct 申请号) as orderTotal from ana_des_20171121 where 申请人国别代码 like '中国' and 申请日 like '%2016%' and 领域 like '机器学习' group by 申请人 order by orderTotal desc limit 10;"
"select 申请年, count(distinct 申请号) as orderTotal from ana_des_20171121_1 where 申请人 like '浙江大学' and 领域 like '机器学习' group by 申请年 order by orderTotal desc limit 3;"

"select 标题,申请日 from ana_des_20171121 where 申请人 like '浙江大学' and 领域 like '机器学习' order by 申请日 desc limit 1;"

"select 标题,申请日 from ana_des_20171121 where 申请人 like '浙江大学' and 领域 like '机器学习' order by 申请日 limit 1;"

"select count(distinct 申请号) from ana_des_20171121 where 申请人 like '浙江大学' and 领域 like '机器学习' and 专利有效性 like '有效';"

"select 标题, 被引次数 from ana_des_20171121 where 申请人 like '浙江大学' and 领域 like '机器学习' order by 被引证次数 desc limit 10;"

"select 申请人, sum(被引证次数) as citedTotal from ana_des_20171121 where 领域 like '机器学习' group by 申请人 order by citedTotal desc limit 10;"

"select 子领域, count(distinct 申请号) as orderTotal from ana_des_20171121 where 申请人 like '浙江大学' and 领域 like '机器学习' group by 子领域 order by orderTotal desc limit 5;"

'''

f = open('question_Organization.txt', 'w+')

time = [2014, 2015, 2016]
country = ['中国', '美国', '日本']
school = ['东华大学', '中南大学', '浙江大学']
field = ['机器学习', '语音识别',]
sub_field1 = ['神经网络', '支持向量机', '主题模型', '深度学习']
sub_field2 = ['声纹识别', '语种识别', '麦克风阵列', '语音合成']

# 16
# f.writelines('16.'+ '【某年】【某机构】在【某领域】的专利申请量是多少'+"\n")
for i in range(len(time)):
    for j in range(len(school)):
        for k in range(len(field)):
            sql = "select count(distinct 申请号) from ana_des_20171121_1 where 申请年 like '%s' and 申请人 like '%s' and 领域 like '%s'" %(time[i], school[j], field[k])
            cur.execute(sql)
            result = cur.fetchall()

            num = result[0][0]
            f.writelines("16,"+"%s年，%s在%s领域的专利申请量是多少, %s年，%s在%s领域的专利申请量为%s篇,"%(time[i], school[j], field[k], time[i], school[j], field[k], num)+"xx"+"\n")

# 17
# f.writelines('17.' + '【某年】【某机构】在【某领域】的专利授权量是多少' + "\n")
for i in range(len(time)):
    for j in range(len(school)):
        for k in range(len(field)):
            sql = "select count(distinct 申请号) from ana_des_20171121_1 where 授权年 like '%s' and 申请人 like '%s' and 领域 like '%s'" %(time[i], school[j], field[k])
            cur.execute(sql)
            result = cur.fetchall()

            num = result[0][0]
            f.writelines("17,"+"%s年，%s在%s领域的专利授权量是多少,%s年，%s在%s领域的专利授权量为%s篇,"%(time[i], school[j], field[k], time[i], school[j], field[k], num)+"xx"+ "\n")



# 19
# f.writelines('19.'+ '【某年】【某机构】在【某领域】的【某国】专利申请量'+"\n")
for i in range(len(time)):
    for j in range(len(school)):
        for k in range(len(field)):
            for c in range(len(country)):
                sql = "select count(distinct 申请号) from ana_des_20171121_1 where 申请年 like '%s' and 申请人 like '%s' and 领域 like '%s' and 申请人国别代码='%s'" %(time[i], school[j], field[k], country[c])
                cur.execute(sql)
                result = cur.fetchall()

                num = result[0][0]
                f.writelines("19,"+"【%s年，%s在%s领域的%s专利申请量是多少,%s年，%s在%s领域的%s专利申请量为%s篇," % (time[i], school[j], field[k], country[c], time[i], school[j], field[k], country[c], num)+"xx"+ "\n")

#  20
# f.writelines('20.'+ '【某年】【某国】【某领域】的专利申请top1机构有哪些'+"\n")
for i in range(len(time)):
    for j in range(len(country)):
        for k in range(len(field)):
            sql = "select 申请人, count(distinct 申请号) as orderTotal from ana_des_20171121_1 where 申请年 like '%s' and 申请人国别代码 like '%s' and 领域 like '%s' group by 申请人 order by orderTotal desc limit 1" %(time[i], country[j], field[k])
            cur.execute(sql)
            result = cur.fetchall()

            if len(result) == 0:
                title = ''
                f.writelines("20,"+"%s年%s在%s领域专利申请top1机构有哪些,%s年%s在%s领域无相关专利," % (time[i], country[j], field[k], time[i], country[j], field[k])+"xx" + "\n")
            else:
                title = result[0][0]
                f.writelines("20,"+"%s年%s在%s领域的专利申请top1机构有哪些,%s年%s在%s领域的专利申请排在第一位的机构是'%s'," % (time[i], country[j], field[k], time[i], country[j], field[k], title)+"xx"+"\n")


#  21
# f.writelines('21.'+'【某机构】在【某领域】专利申请量最多的年份'+ "\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select 申请年, count(distinct 申请号) as orderTotal from ana_des_20171121_1 where 申请人 like '%s' and 领域 like '%s' group by 申请年 order by orderTotal desc limit 1" % (school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        num = result[0][0]
        f.writelines("21,"+"%s在%s领域专利申请量最多的年份是哪一年,%s在%s领域专利申请量最多的年份为%s年," % (school[i], field[j], school[i], field[j], num)+"xx"+"\n")

#  22
# f.writelines('22.'+ '【某机构】在【某领域】最新申请的专利'+"\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select 标题,申请日 from ana_des_20171121 where 申请人 like '%s' and 领域 like '%s' order by 申请日 desc limit 1" %(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (school[i], field[j])+ "\n")
        else:
            title = result[0][0]
            f.writelines("22,"+"%s在%s领域最新申请的专利是什么,%s在%s领域最新申请的专利是'%s'," % (school[i], field[j], school[i], field[j], title)+"xx"+"\n")

#  23
# f.writelines('23.'+'【某机构】在【某领域】最早申请的专利'+ "\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select 标题,申请日 from ana_des_20171121 where 申请人 like '%s' and 领域 like '%s' order by 申请日 limit 1" %(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (school[i], field[j])+ "\n")
        else:
            title = result[0][0]
            f.writelines("23,"+"%s在%s领域最早申请的专利是什么,%s在%s领域最早申请的专利是'%s'," % (school[i], field[j], school[i], field[j], title)+"xx"+ "\n")


#  25
# f.writelines('25.'+'【某机构】在【某领域】的有效专利数量'+ "\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select count(distinct 申请号) from ana_des_20171121 where 申请人 like '%s' and 领域 like '%s' and 专利有效性 like '有效'" %(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        num = result[0][0]
        f.writelines("25,"+"%s在%s领域的有效专利数量是多少,%s在%s领域的有效专利数量为%s篇," %(school[i], field[j], school[i], field[j], num)+"xx"+"\n")
#
#  26
# f.writelines('26.'+'【某机构】在【某领域】的三方专利数量'+ "\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select count(distinct 申请号) from ana_des_20171121_1 where 申请人 like '%s' and 领域 like '%s' and 简单同族 REGEXP 'JP|US|CN'" %(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        num = result[0][0]
        f.writelines("26,"+"%s在%s领域的三方专利数量是多少,%s在%s领域的三方专利数量为%s篇," % (school[i], field[j], school[i], field[j], num)+"xx"+"\n")
#
#  28
# f.writelines('28.'+'【某机构】在【某领域】的topn高被引专利'+ "\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select 标题 from ana_des_20171121_1 where 申请人 like '%s' and 领域 like '%s' order by 被引证次数 desc limit 1;"%(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) == 0:
            title = ''
            f.writelines("%s在%s领域无相关专利" % (school[i], field[j])+ "\n")
        else:
            title = result[0][0]
            f.writelines("28,"+"%s在%s领域的top1高被引专利是什么,%s在%s领域的top1高被引专利是'%s'," % (school[i], field[j], school[i], field[j], title)+"xx"+"\n")

# 29
# f.writelines('29.' + '【某领域】的高被引topn机构' + "\n")
for j in range(len(field)):
    sql = "select 申请人, sum(被引证次数) as citedTotal from ana_des_20171121 where 领域 like '%s' group by 申请人 order by citedTotal desc limit 1" % (field[j])
    cur.execute(sql)
    result = cur.fetchall()

    num = result[0][0]
    f.writelines("29,"+"%s领域的高被引机构top1是哪家机构,%s领域的高被引机构top1是'%s'," % (field[j], field[j], num) + "xx"+"\n")

# #  30
# f.writelines('30.'+ '【某机构】在【某领域】的主要研究方向'+"\n")
for i in range(len(school)):
    for j in range(len(field)):
        sql = "select 子领域, count(distinct 申请号) as num from ana_des_20171121_1 where 申请人 like '%s' and 领域 like '%s' group by 子领域 order by num desc limit 2;" %(school[i], field[j])
        cur.execute(sql)
        result = cur.fetchall()

        num = result[0][0]
        f.writelines("30,"+"%s在%s领域的主要研究方向是什么,%s在%s领域的主要研究方向是%s," % (school[i], field[j], school[i], field[j], num)+"xx"+ "\n")

        # if len(result) == 0:
        #     title = ''
        #     f.writelines("%s在%s领域无相关专利" % (school[i], field[j])+ "\n")
        # else:
        #     subdomain = []
        #     for i in result:
        #         sd = i[0]
        #         subdomain.append(sd)
        #     text = '、'.join(subdomain)
        #     f.writelines("%s在%s领域的主要研究方向是%s" % (school[i], field[j], text)+ "\n")

# while True:
#     line = f.readline()
#     line = line.strip('\n')
#     line = line.split(",")
#     print line
    # ID = line[0]
    # question = line[1]
    # print question
    # answer = line[2]
    # print answer
    # author = line[3]
#     cur.execute("insert into ans_des_result_20171123(id,question,answer,author) values(%s,%s,%s,%s)", [ID, question, answer, author])
# f.close()
# cur.close()
# conn.commit()
# conn.close()




