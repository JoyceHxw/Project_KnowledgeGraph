from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result(request):
    global graph
    name=request.GET.get('name','')
    # 模糊查询所有名字相关的节点
    # 按匹配程度排序
    query="""
        match (n)
        where n.name contains $name or $name contains n.name
        return n,labels(n) AS label
        ORDER BY 
            CASE WHEN n.name = $name THEN 1   // 完全匹配
                WHEN n.name STARTS WITH $name THEN 2  // 以 "Alice" 开头
                when n.name ends with $name then 3
                ELSE 4  // 其他情况
            END;
        """
    parameters = {"name": name}
    all_relative_nodes=graph.run(query,parameters).data()
    all_relative_nodes_json=json.dumps(all_relative_nodes,ensure_ascii=False)
    context={
        "search":name,
        "all_relative_nodes_json":all_relative_nodes_json
    }
    return render(request,'search_all.html',context)