from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import spacy
import json
from py2neo import Graph
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])
nlp = spacy.load('./chatbot/model')

def index(request):
    if request.method == "POST":
        # 获取用户输入问题
        data = json.loads(request.body.decode("utf-8"))  # 解析 JSON 数据
        question = data.get("question", "")  
        # 使用模型处理问题
        doc = nlp(question)
        answer = process_model_output(doc)  # 处理模型输出以获得答案
        # 返回答案到前端页面
        context = {"question": question, "answer": answer}
        # 返回json数据格式!JsonResponse渲染
        return JsonResponse(context)

    return render(request,'index.html')

def process_model_output(doc):
    answer=None
    key_word=None
    labels={'股东':'Shareholder','公司':'Company','高管':'Executive','行业':'Industry','地域':'Region'}
    for token in doc:
        token_text = token.text
        if token_text in labels:
            key_word=labels[token_text]
            break
    try:
        # 实体
        name=doc.ents[0].text
        # 标签
        label=doc.ents[0].label_
    except:
        name=None
        label=None
    print(name)
    print(label)
    print(key_word)
    if key_word!=None:
        query="""
            match (n)-[r]-(m)
            where ($name contains n.name or n.name contains $name) and labels(m) = [$key_word]
            return n.name,type(r) as rel,m.name
            """
        parameters={"name":name,"key_word":key_word}
        answer_list=[]
        result=graph.run(query,parameters).data()
        for record in result:
            answer_list.append(record["m.name"])
    else:
        query="""
            match (n)
            where ($name contains n.name or n.name contains $name) 
            return n.name, n.age, n.gender, n.education, n.incorporation_date, n.listing_date, n.introduction
            """
        parameters={"name":name,"key_word":key_word}
        answer_list=[]
        result=graph.run(query,parameters).data()
        for record in result:
            if record.get("n.name"):
                answer_list.append(record.get("n.name"))
            if record.get("n.age"):
                answer_list.append("年龄："+record.get("n.age"))
            if record.get("n.gender"):
                answer_list.append("性别："+record.get("n.gender"))
            if record.get("n.education"):
                answer_list.append("教育程度："+record.get("n.education"))
            if record.get("n.incorporation_date"):
                answer_list.append("成立日期："+record.get("n.incorporation_date"))
            if record.get("n.listing_date"):
                answer_list.append("上市日期："+record.get("n.listing_date"))
            if record.get("n.introduction"):
                answer_list.append(record.get("n.introduction"))
            answer_list.append('\n')
    
    answer=", ".join(answer_list)
    if answer=="":
        return "抱歉，无法查到相关信息，请换个提问方式"
    return answer
