import re
from datetime import datetime

import CreateQA_main as QA
import sys

country=list()
field=list()
sub_field=dict()
person=list()
key_in_types=dict()

# 根据得到的关键词，得到答案文本。sql检索法
def reply(keywords):
    QA.init()
    answer_templates = QA.get_answer_templates(keywords['type'])
    answers=list()
    for answer_template in answer_templates:
        answers.append(QA.fill_answer(answer_template["content"],keywords))
    return answers

def reply2(keywords):
    QA.init()
    answer_templates = QA.get_answer_templates(keywords['type'])
    answers = list()
    for answer_template in answer_templates:
        answers.append(QA.fill_answer(answer_template["content"], keywords))
    return answers

# 初始化。读入各种规则列表
def init():
    f=open("dict/country_list.txt",mode="r",encoding="utf-8")
    global country
    for item in f.readlines():
        if len(item.strip())>0: country.append(item.strip().replace('\r',''))

    f = open("dict/field_list.txt", mode="r", encoding="utf-8")
    global field,sub_field
    fielditem = f.readlines()
    for item in fielditem:
        if len(item.strip()) > 0:
            pair=item.strip().replace('\r','').split('\t')
            if pair[0] not in field:field.append(pair[0])
            sub_field[pair[1]]=pair[0]

    f=open("dict/person_list.txt",mode="r",encoding="utf-8")
    global person
    for item in f.readlines():
        if len(item.strip()) > 0: person.append(item.strip().replace('\r',''))

    f = open("dict/question_key.txt", mode="r", encoding="utf-8")
    global key_in_types
    for item in f.readlines():
        if len(item.strip()) > 0:
            pair=item.strip().replace('\r','').split('\t')
            if len(pair)==4:
                key_in_types[pair[0]]=pair[1:4]

def get_year(text):
    pattern1 = re.compile(r'\d{4}年')
    pattern2 = re.compile(r'[^\d]?\d{2}年')
    res=''
    for pos in range(0,len(text)):
        match1 = pattern1.search(text, pos)
        match2 = pattern2.search(text, pos)
        if match1:
            s = match1.start()
            e = match1.end()
            res = text[s:e - 1]
            break
        elif match2:
            s = match2.start()
            e = match2.end()
            res = text[s:e - 1]
            break
        elif '今年' in text[pos:]:
            res = str(datetime.now().year)
            break
        elif '去年' in text[pos:]:
            res = str(datetime.now().year - 1)
            break
        elif '前年' in text[pos:]:
            res = str(datetime.now().year - 2)
            break
    return res

def get_num(text):
    pattern1 = re.compile(r'前(\d{1}|[一二两三四五六七八九十]{1})')
    res = ''
    for pos in range(0, len(text)):
        match1 = pattern1.search(text, pos)
        if match1:
            s = match1.start()
            e = match1.end()
            res = text[s+1:e]
            break
    return str(res)

# 是否包含该关键词
# 以后可能改成模糊匹配之类
def have_key(question,key):
    if key in question:
        return True
    return False

# 由于某些问题无法根据关键词做区分，因此返回的有可能是多个问题的列表
def get_types(question,keys):
    type=[]
    q=question
    # print(keys)
    for key in keys:
        for k in keys[key]:
            q=q.replace(k,'')

    # print(keys,q_key)

    keystr=''
    keystr += ('1' if 'country' in keys else'0')
    keystr += ('1' if 'year' in keys else'0')
    keystr += ('1' if 'person' in keys else'0')
    keystr += ('1' if 'topn' in keys else'0')

    # print(keystr,''.join(q_key[0][1:5]))
    for q_type in key_in_types:
        # print(keystr , key[2])
        key=key_in_types[q_type]
        if    keystr == key[1]  and have_key(question,key[0]):
            type.append(q_type)
    return type

# 将输入的文本进行分析，得到关键词和问题类型
def get_keywords(question):
    keywords_list=[]

    cname=[]
    fname=[]
    sfname=[]
    pname=[]
    year=[]
    topn=[]

    # 判断国家关键词
    for c in country:
        if c in question:
            cname.append(c)
            # break
    real_country=''
    for c in cname:
        if len(real_country)<len(c):
            real_country=c
    if len(real_country) > 0:
        cname = [real_country]
    else:
        cname = []

    # 判断领域关键词
    for f in field:
        # print(f)
        if f in question:
            fname.append(f)
            # break
    real_field = ''
    for f in fname:
        if len(real_field) < len(f):
            real_field = f
    if len(real_field) > 0:
        fname = [real_field]
    else:
        fname = []


    # 判断子领域关键词
    for sf in sub_field.keys():
        if sf in question:
            if len(fname)<=0: fname.append(sub_field[sf])
            sfname.append(sf)
            # break
    real_sfield = ''
    for f in sfname:
        if len(real_sfield) < len(f):
            real_sfield = f
    if len(real_sfield) > 0:
        sfname = [real_sfield]
    else:
        sfname = []


    # 判断人名
    for p in person:
        if p in question:
            pname.append(p)

    # 判断年份
    year_tmp=get_year(question)
    if len(year_tmp) > 0:year.append(year_tmp)

    # 判断topn数
    topn_tmp=get_num(question)
    num_han2int={'一':1,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
    if topn_tmp in num_han2int: topn_tmp=str(num_han2int[topn_tmp])
    if len(topn_tmp)>0 :topn.append(topn_tmp)

    tmpk={}
    if len(cname) >= 1:tmpk['country']=cname
    if len(fname)>=1:tmpk['field']=fname
    elif len(sfname)>=1 and sfname in sub_field:tmpk['field']=sub_field[sfname]
    if len(pname) >= 1:tmpk['person']=pname
    if len(year) >= 1:tmpk['year']=year
    if len(topn) >= 1:tmpk['topn']=topn

    types = get_types(question,tmpk)

    print(cname,fname,sfname,pname,year,topn,types)

    tmpk['type']=types
    # print(tmpk)
    for t in types:

        keywords = {}
        if len(t) >= 1: keywords['type']=t
        # print(key_in_types[t])
        type_key_code=key_in_types[t][2]
        if len(year) >= 1 and type_key_code[0]=='1': keywords['优先权年'] = year[0]
        if len(year) >= 1 and type_key_code[1]=='1':  keywords['授权年'] = year[0]
        if len(year) >= 1 and type_key_code[2]=='1': keywords['申请年'] = year[0]
        if len(cname) >= 1 and type_key_code[3]=='1':  keywords['来源国'] = cname[0]
        if len(cname) >= 1 and type_key_code[4]=='1': keywords['流向国'] = cname[0]
        if len(fname) >= 1 and type_key_code[5]=='1': keywords['领域'] = fname[0]
        if len(sfname) >= 1 and type_key_code[6]=='1': keywords['子领域'] = sfname[0]
        if len(pname) >= 1 and type_key_code[7]=='1': keywords['申请人'] = pname[0]
        if len(pname) >= 2 and type_key_code[8]=='1': keywords['发明人'] = pname[1]
        if len(topn) >= 1 and type_key_code[9]=='1': keywords['topN数目'] = topn[0]
        keywords_list.append(keywords)

    return keywords_list

if __name__ == '__main__':
    init()
    question=sys.argv[0]
    question="美国在2017年的语音处理的专利申请量是多少？"
    # get_keywords(question)
    # get_keywords("今年，中国在语音处理领域的专利申请量是多少？南通同洲电子有限责任公司麦克风阵列")
    qs=get_keywords(question)
    for q in qs:
        # print(q['type'])
        answers = reply(q)
        for answer in answers:
            print(answer)
    # for answer in answers:
    #     print(answer)
