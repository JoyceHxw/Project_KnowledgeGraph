import spacy
import zh_core_web_sm
import pandas as pd
from spacy.training.example import Example
import random

def get_train_data():
    companies=pd.read_csv('./data_process/company_processed.csv',usecols=['name'])
    shareholders=pd.read_csv('./data_process/shareholder_processed.csv',usecols=['name'])
    executives=pd.read_csv('./data_process/executive_processed.csv',usecols=['name'])
    industries=pd.read_csv('./data_process/industry_processed.csv',usecols=['name'])
    regions=pd.read_csv('./data_process/region_processed.csv',usecols=['name'])

    # 整合数据
    data = []

    # for company in companies['name']:
    #     data.append((f"{company}的股东有哪些", {"entities": [(0, len(company), "COMPANY")]}))

    # for shareholder in shareholders['name']:
    #     data.append((f"{shareholder}投资了哪些公司?", {"entities": [(0, len(shareholder), "SHAREHOLDER")]}))

    # for executive in executives['name']:
    #     data.append((f"{executive}在哪家公司任职", {"entities": [(0, len(executive), "EXECUTIVE")]}))

    for industry in industries['name']:
        data.append((f"{industry}有多少家公司", {"entities": [(0, len(industry), "INDUSTRY")]}))

    for region in regions['name']:
        data.append((f"{region}有多少家公司", {"entities": [(0, len(region), "REGION")]}))
    return data

train_data=get_train_data()
# print(train_data)
# nlp=spacy.load('zh_core_web_sm')
# ner=nlp.get_pipe("ner")
nlp=spacy.load('./chatbot/model')


# for label in ["COMPANY","SHAREHOLDER", "EXECUTIVE", "INDUSTRY", "REGION"]:
#     ner.add_label(label)

num_iterations = 1
for i in range(num_iterations):
    random.shuffle(train_data)
    for text, annotations in train_data:
        example=Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0)

nlp.to_disk("./chatbot/model")
