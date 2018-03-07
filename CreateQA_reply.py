import CreateQA_main as QA
import sys



def reply(keywords):
    QA.init()
    answer_templates = QA.get_answer_templates(keywords['type'])
    answers=list()
    for answer_template in answer_templates:
        answers.append(QA.fill_answer(answer_template["content"],keywords))
    return answers

def get_keywords(question):
    keywords={}
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


    # keywords['']



    return keywords

if __name__ == '__main__':
    question=sys.argv[0]
    answers = reply(get_keywords(question))
    for answer in answers:
        print(answer)
