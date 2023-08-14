from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result(request):
    global graph
    name = request.GET.get('name', '')
    age = request.GET.get('age', '')
    # 高管基本信息
    query_basic = """
            match (n:Executive) 
            where n.name=$name and n.age=$age
            return n.name,n.gender,n.age,n.education
            """
    parameters = {"name": name,"age":age}
    executive_basic = graph.run(query_basic, parameters).data()
    if executive_basic:
        executive_basic = executive_basic[0]
        executive_name = executive_basic.get("n.name")
        executive_gender = executive_basic.get("n.gender")
        executive_education = executive_basic.get("n.education")
        executive_age = executive_basic.get("n.age")


    else:
        executive_name = None
        executive_gender = None
        executive_education = None
        executive_age = None


    executive_basic_info = {
        "executive_name": executive_name,
        "executive_gender": executive_gender,
        "executive_education": executive_education,
        "executive_age": executive_age,
    }

    query_executive = """match (m:Executive)-[r:MANAGE]->(n:Company)
                                where m.name=$name and m.age=$age
                                return m,r,n
                                """
    company_executive = graph.run(query_executive, parameters).data()
    company_executive_json = json.dumps(company_executive, ensure_ascii=False)

    executive_info = {
        "executive_basic_info": executive_basic_info,
        "company_executive_json": company_executive_json,
        "name":name,
        "age":age
    }

    return render(request, 'executive.html', executive_info)
