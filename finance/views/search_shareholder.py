from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result(request):
    global graph
    name = request.GET.get('name', '')
    # 股东基本信息
    query_basic = """
                match (n:Shareholder) 
                where n.name=$name
                return n.name
                """
    parameters = {"name": name}
    shareholder_basic = graph.run(query_basic, parameters).data()
    if shareholder_basic:
        shareholder_basic = shareholder_basic[0]
        shareholder_name = shareholder_basic.get("n.name")
    else:
        shareholder_name=None;
    shareholder_basic_info = {
        "shareholder_name": shareholder_name,
    }
    query_shareholder = """match (m:Shareholder)-[r:INVEST]->(n:Company)
                        where m.name=$name
                        return m,r,n
                        """
    company_shareholder = graph.run(query_shareholder, parameters).data()
    company_shareholder_json = json.dumps(company_shareholder, ensure_ascii=False)

    shareholder_info = {
        "shareholder_basic_info": shareholder_basic_info,
        "company_shareholder_json": company_shareholder_json,
        "name":name
    }
    return render(request, 'shareholder.html', shareholder_info)
