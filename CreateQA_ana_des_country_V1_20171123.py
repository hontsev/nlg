#!usr/bin/python
# encoding=utf8
# author: wangyanpeng
# data: 2017/11/23
# function: 国家问答模板生成
# input: MySQL[114.115.149.84],db[ANA_DES_20171121]
# output:问句及答句语料



import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import pymysql
import pymysql.cursors
import pandas as pd

#连接配置信息
config = {
          'host':'127.0.0.1',
          'port':3306,#MySQL默认端口
          'user':'root',#mysql默认用户名
          'password':'3512134',
          'db':'jw_test',#数据库
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }

# 创建连接
con= pymysql.connect(**config)

# 定义模版的空缺数据
years=[2014,2015,2016]
countrys=["中国","美国","日本"]
scientists=["周明杰","陈庆","戴加龙"]
institutes=["东华大学","中南大学","浙江大学"]
shouli_countrys=["CN","US","JP"]
shouli_chinese={"CN":"中国","US":"美国","JP":"日本"}
areas=["机器学习","语音识别"]
sub_area_mls=["神经网络","支持向量机","主题模型","深度学习"]
sub_area_srs=["声纹识别","语种识别","麦克风阵列","语音合成"]


# 模版id_1 【某年】【某国】在【某领域】的专利申请量
def id_1(year_list,country_list,sub_area_list):
    with con.cursor() as cursor:
        for year in year_list:
            for country in country_list:
                for sub_area in sub_area_list:
                    sql = "SELECT COUNT(DISTINCT `申请号`) as app_number " \
                          "FROM `ana_des_20171121_1` " \
                          "where `申请人国别代码` like '%%%s%%' and `申请年`='%s' and `子领域`='%s'" % (str(country), str(year), str(sub_area))
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    print '1 Q：'+str(year)+'年,'+str(country)+'在'+str(sub_area)+'领域的专利申请量为多少？      '\
                          +'A：'+str(year)+'年,'+str(country)+'在'+str(sub_area)+'领域的专利申请量为'+str(result[0][u'app_number'])+'件'

# 模版id_2  【某年】【某国】在【某领域】的专利授权量
def id_2(year_list,country_list,sub_area_list):
    with con.cursor() as cursor:
        for year in year_list:
            for country in country_list:
                for sub_area in sub_area_list:
                    sql = "SELECT COUNT(DISTINCT `申请号`) as grant_number " \
                          "FROM `ana_des_20171121_1` " \
                          "where `申请人国别代码` like '%%%s%%' and `授权公告日` like '%s%%' and `子领域`='%s'" % (str(country), str(year), str(sub_area))
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    print '2 Q：'+str(year)+'年,'+str(country)+'在'+str(sub_area)+'领域的专利授权量为多少？      '\
                          +'A：'+str(year)+'年,'+str(country)+'在'+str(sub_area)+'领域的专利授权量为'+str(result[0][u'grant_number'])+'件'

# 模版id_4  【某年】【某机构】在【某领域】的【某国】专利申请量
def id_4(year_list,institute_list,area_list,shouli_country_list):
    with con.cursor() as cursor:
        for year in year_list:
            for institute in institute_list:
                for area in area_list:
                    for shouli_country in shouli_country_list:
                        sql = "SELECT COUNT(DISTINCT `申请号`) as app_number " \
                              "FROM `ana_des_20171121_1` " \
                              "where `申请人` like '%%%s%%' and `申请年` = '%s' and `领域`='%s' and `申请号` like '%s%%'" \
                              % (str(institute), str(year), str(area),str(shouli_country))
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        print '4 Q：' + str(year) + '年,' + str(institute) + '在' + str(area) + '领域的'+str(shouli_chinese[shouli_country])+'专利申请量为多少？      ' \
                              + 'A：' + str(year) + '年,' + str(institute) + '在' + str(area) + '领域的'+str(shouli_chinese[shouli_country])+'专利申请量为' + str(result[0][u'app_number']) + '件'

# id_5 【某领域】专利申请量topn国家
def id_5(sub_area_list,year_list,n):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for year in year_list:
                sql = "SELECT `申请人国别代码` " \
                      "FROM ( SELECT `申请人国别代码`, COUNT(DISTINCT `申请号`) AS 专利数量 " \
                      "FROM `ana_des_20171121_1` " \
                      "WHERE `子领域` = '%s' and `申请年`='%s' GROUP BY `申请人国别代码` ORDER BY `专利数量` DESC) AS paixubiao " \
                      "LIMIT %s" % (str(sub_area), year, n)
                cursor.execute(sql)
                result = cursor.fetchall()
                top_country_list = []
                for item in result:
                    top_country_list.append(item[u'申请人国别代码'])
                print '5 Q：' + str(year)+ '年,' + str(sub_area) + '领域专利申请量Top' + str(n) + '的国家是哪些？  ' \
                      + 'A：' + str(year)+ '年,'+ str(sub_area) + '领域专利申请量Top' + str(n) + '的国家是' + ','.join(top_country_list)

# id_6  【某国】在【某领域】专利申请量最多的年份
def id_6(country_list,sub_area_list):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="select `申请年` FROM (SELECT `申请年`,COUNT(DISTINCT `申请号`) AS 专利数量 FROM `ana_des_20171121_1` where `申请人国别代码` like '%%%s%%' and `子领域`='%s' GROUP BY `申请年` ORDER BY `专利数量` DESC) as paixubiao LIMIT 1" % (str(country),str(sub_area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '6 Q：' + str(country)+'在'+str(sub_area)+'专利申请量最多的年份是哪年？      ' \
                      + 'A：' + str(country)+'在'+str(sub_area)+'专利申请量最多的年份是'+str(result[0][u'申请年'])+'年'

# id_7 【某国】在【某领域】最新申请的专利  问题：按照日期排序时，日期被当作字符串排序
def id_7(country_list,sub_area_list):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="SELECT `标题`,`申请日` FROM `ana_des_20171121_1` where `申请人国别代码` like '%%%s%%' and `子领域`='%s' ORDER BY `申请日` desc limit 1" % (str(country),str(sub_area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '7 Q：' + str(country) + '在' + str(sub_area) + '领域最新申请的专利是什么？      ' \
                      + 'A：' + str(country) + '在' + str(sub_area) + '领域最新申请的专利是“' + str(result[0][u'标题'])+'”，申请日期为：'+str(result[0][u'申请日'])

# id_8 【某国】在【某领域】最早申请的专利  问题：按照日期排序时，日期被当作字符串排序
def id_8(country_list,sub_area_list):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="SELECT `标题`,`申请日` FROM `ana_des_20171121_1` where `申请人国别代码` like '%%%s%%' and `子领域`='%s' ORDER BY `申请日`  limit 1" % (str(country),str(sub_area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '8 Q：' + str(country) + '在' + str(sub_area) + '领域最早申请的专利是什么？      ' \
                      + 'A：' + str(country) + '在' + str(sub_area) + '领域最早申请的专利是“' + str(result[0][u'标题'])+'”，申请日期为：'+str(result[0][u'申请日'])

# id_10 【某国】在【某领域】的有效专利数量
def id_10(country_list,sub_area_list):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="select count(distinct `申请号`) AS 有效专利数量 from ana_des_20171121_1 where `申请人国别代码` like '%%%s%%' and `子领域`='%s' and `专利有效性`='有效'" % (str(country),str(sub_area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '10 Q：' + str(country) + '在' + str(sub_area) + '领域的有效专利数量是多少？      ' \
                      + 'A：' + str(country) + '在' + str(sub_area) + '领域的有效专利数量是' + str(result[0][u'有效专利数量'])+'件'

# id_11 【某国】在【某领域】的三方专利数量
def id_11(country_list,area_list):
    with con.cursor() as cursor:
        for area in area_list:
            for country in country_list:
                sql="SELECT COUNT(DISTINCT `申请号`) as 三方专利数量 FROM `ana_des_20171121_1` where `简单同族` like '%%%s%%' and `简单同族` like '%%%s%%' and `简单同族` like '%%%s%%' and `申请人国别代码` like '%%%s%%' and `领域`='%s'" % ('CN','JP','US',str(country),str(area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '11 Q：' + str(country) + '在' + str(area) + '领域的三方（中、美、日）专利数量是多少？      ' \
                      + 'A：' + str(country) + '在' + str(area) + '领域的三方（中、美、日）专利数量是' + str(result[0][u'三方专利数量'])+'件'

# id_12 【某国】在【某领域】的主要技术产出力量
def id_12(country_list,sub_area_list):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="SELECT `申请人类型`,COUNT(DISTINCT `申请号`) as 专利数量 FROM `ana_des_20171121_1` where `申请人国别代码` like '%%%s%%' and `子领域`='%s' GROUP BY `申请人类型` ORDER BY `专利数量` DESC" % (str(country),str(sub_area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '12 Q：' + str(country) + '在' + str(sub_area) + '的主要技术产出力量？      ' \
                      + 'A：' + str(country) + '在' + str(sub_area) + '的主要技术产出力量是' + str(result[0][u'申请人类型'])


# id_14 【某国】在【某领域】的topn高被引专利
def id_14(country_list,sub_area_list,n):
    with con.cursor() as cursor:
        for sub_area in sub_area_list:
            for country in country_list:
                sql="SELECT `标题` FROM `ana_des_20171121_1` WHERE `申请人国别代码` like '%%%s%%'  and `子领域`='%s' ORDER BY `被引证次数` desc limit %s" % (str(country),str(sub_area),n)
                cursor.execute(sql)
                result = cursor.fetchall()
                title_list=[]
                for item in result:
                    title_list.append(item[u'标题'])
                print '14 Q：' + str(country) + '在' + str(sub_area) + '领域的Top'+str(n)+'高被引专利？      ' \
                    + 'A：' + str(country) + '在' + str(sub_area) + '领域的Top'+str(n)+'高被引专利是' + ','.join(title_list)

# id_15 【某国】在【某领域】的主要研究方向
def id_15(country_list,area_list):
    with con.cursor() as cursor:
        for area in area_list:
            for country in country_list:
                sql="SELECT `子领域`,COUNT(DISTINCT `申请号`) AS 专利数量 FROM `ana_des_20171121_1` WHERE `申请人国别代码` like '%%%s%%' and `领域`='%s' GROUP BY `子领域` ORDER BY `专利数量` DESC" % (str(country),str(area))
                cursor.execute(sql)
                result = cursor.fetchall()
                print '15 Q：' + str(country) + '在' + str(area) + '领域的主要研究方向是什么？      '       \
                    + 'A：' + str(country) + '在' + str(area) + '领域的主要研究方向是'+str(result[0][u'子领域'])




if __name__ == '__main__':
    id_1(years, countrys, sub_area_mls)
    id_2(years, countrys, sub_area_srs)
    id_4(years,institutes,areas,shouli_countrys)
    id_5(sub_area_mls,years,5)
    id_6(countrys, sub_area_mls)
    id_7(countrys, sub_area_mls)
    id_8(countrys, sub_area_mls)
    id_10(countrys, sub_area_mls)
    id_12(countrys, sub_area_mls)
    id_14(countrys, sub_area_mls,3)
    id_15(countrys, areas)

con.close()