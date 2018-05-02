import CreateQA_main as QA
import sys
from flask import Flask

app = Flask(__name__)
@app.route('/<question>',methods=['GET','POST'])
def answer_it(question):
    generator = QA.QAGenerator()
    answer = generator.answer(question)
    return answer

if __name__ == '__main__':
    # app.run(debug=True)

    g=QA.QAGenerator()
    question = "20171年，清华大学的有关语音处理的专利申请量有多少呢？"
    a=g.answer(question)
    print(a)

