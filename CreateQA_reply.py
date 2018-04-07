import re

import CreateQA_main as QA
import sys

country=list()
field=list()
sub_field=dict()
person=list()

# 根据得到的关键词，得到答案文本
def reply(keywords):

    QA.init()
    answer_templates = QA.get_answer_templates(keywords['type'])
    answers=list()
    for answer_template in answer_templates:
        answers.append(QA.fill_answer(answer_template["content"],keywords))
    return answers

# 初始化。读入各种规则列表
def init():
    f=open("countries.txt",mode="r",encoding="utf-8")
    global country
    for item in f.readlines():country.append(item.strip())

    f = open("fields.txt", mode="r", encoding="utf-8")
    global field,sub_field
    fielditem = f.readlines()
    for item in fielditem:
        pair=item.strip().split('\t')
        if pair[0] not in field:field.append(pair[0])
        sub_field[pair[1]]=pair[0]

    f=open("persons.txt",mode="r",encoding="utf-8")
    global person
    for item in f.readlines():person.append(item.strip())


def get_year(text):
    pattern = re.compile(r'\d{4}年')
    pos = -1
    res=''
    while True:
        match = pattern.search(text, pos)
        if not match:
            break
        res=text[s,e-1]
        s = match.start()
        e = match.end()
        pos = e
    return [pos,res]

    # 将输入的文本进行分析，得到关键词和问题类型
def get_keywords(question):
    keywords={}
    cname=""
    fname=""
    sfname=""
    pname=""
    for c in country:
        if c in question:
            cname=c
            break
    for f in field:
        # print(f)
        if f in question:
            fname=f
            break
    for sf in sub_field.keys():
        if sf in question:
            fname=sub_field[sf]
            sfname=sf
            break
    for p in person:
        if p in question:
            pname = p
            break

    print("%s,%s,%s,%s" % (cname,fname,sfname,pname))









    keywords['type']=1
    keywords['优先权年'] = '2017'
    keywords['授权年'] = '2017'
    keywords['申请年'] = '2016'
    keywords['来源国'] = '中国'
    keywords['流向国'] = '中国'
    keywords['领域'] = '人工智能'
    keywords['子领域'] = '深度学习'
    keywords['申请人'] = '张三'
    keywords['发明人'] = '李四'
    keywords['topN数目'] = 3






    return keywords

if __name__ == '__main__':
    init()
    question=sys.argv[0]
    question="2016年，中国在语音处理领域的专利申请量是多少？南通同洲电子有限责任公司麦克风阵列"
    answers = reply(get_keywords(question))
    for answer in answers:
        print(answer)
