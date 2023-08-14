from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result(request):
    global graph
    name=request.GET.get('name','')
    # 行业基本信息
    query_basic = """
        match (n:Industry) 
        where n.name=$name 
        return n.name
        """
    parameters={"name":name}
    industry_basic=graph.run(query_basic,parameters).data()
    if industry_basic:
        industry_basic=industry_basic[0]
        industry_name=industry_basic.get("n.name")
    else:
        industry_name=None

    industry_basic_info={
        "industry_name":industry_name,
    }
    
    # 公司信息
    query_company="""
        match (m:Company)-[r:BELONGTO]->(n:Industry) 
        where n.name=$name 
        return m,r,n
        """
    industry_company=graph.run(query_company,parameters).data()
    industry_company_json=json.dumps(industry_company,ensure_ascii=False)
    
    industry_info={
        "industry_basic_info":industry_basic_info,
        "industry_company_json":industry_company_json,
        "name":name
    }
    return render(request,'industry.html',industry_info)