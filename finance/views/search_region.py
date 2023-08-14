from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result(request):
    global graph
    name=request.GET.get('name','')
    # 地域基本信息
    query_basic = """
        match (n:Region) 
        where n.name=$name 
        return n.name
        """
    parameters={"name":name}
    region_basic=graph.run(query_basic,parameters).data()
    if region_basic:
        region_basic=region_basic[0]
        region_name=region_basic.get("n.name")
    else:
        region_name=None
        
    region_basic_info={
        "region_name":region_name,
    }
    
    # 公司信息
    query_company="""
        match (m:Company)-[r:LOCATE]->(n:Region) 
        where n.name=$name 
        return m,r,n
        """
    region_company=graph.run(query_company,parameters).data()
    region_company_json=json.dumps(region_company,ensure_ascii=False)

    region_info={
        "region_basic_info":region_basic_info,
        "region_company_json":region_company_json,
        "name":name
    }
    return render(request,'region.html',region_info)