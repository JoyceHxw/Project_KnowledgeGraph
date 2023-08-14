import spacy
import json


nlp=spacy.load('./chatbot/model')
text_list=["海天味业的高管是谁?"
           ,"绿盟科技的股东是谁"
           ,"郭永清在哪家公司任职?"
           ,"郭永清多少岁"
           ,"汽车行业有哪些公司?"
           ,"中华人民共和国财政部投资了哪些公司?"
           ,"有多少家公司在四川?"
           ,"上海有多少家上市公司"]
# text="保险是一个行业"
for text in text_list:
    doc=nlp(text)
    # for token in doc:
    #     print(f"词: {token.text}, 词性: {token.pos_}, 依存关系: {token.dep_}")
    for ent in doc.ents:
        print(f"实体: {ent.text}, 类别: {ent.label_}")
