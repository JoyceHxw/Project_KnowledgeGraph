# 上市公司知识图谱项目 #
### 项目功能 ###
- 搜索功能：支持上市公司、股东、高管、行业、地域的搜索
- 关系查询功能：可视化显示上市公司、股东、高管之间的关系
- 上市公司综合评价功能：给行业的每一家公司进行评分，帮助用户掌握上市公司状况
- 智能问答功能：回答用户关于上市公司的问题
### 技术栈 ###
#### 前端 ####
- bootstrap框架
- ajax发送请求
- Echarts可视化呈现
#### 后端 ####
- django框架
- mysql数据库存储用户信息
- neo4j数据库存储上市公司相关信息
- python-pandas/numpy/spacy对数据进行处理分析
### 文件说明 ###
- mysite是django配置文件
- finance是django项目框架
- crawl是运用selenium从东方财富网站爬取上市公司相关数据
- data_process是运用pandas进行数据处理并导入neo4j数据库
- chatbot是运用spacy训练上市公司实体标签，实现简单的问答功能
- evaluation是运用topsis方法实现上市公司综合评价功能
### 页面展示 ###
- 主页面
![](https://github.com/JoyceHxw/Project_KnowledgeGraph/blob/main/index_demo.png)
- 关系图
![](https://github.com/JoyceHxw/Project_KnowledgeGraph/blob/main/structure_demo.png)
- 评价功能
![](https://github.com/JoyceHxw/Project_KnowledgeGraph/blob/main/evaluation_demo.png)
- 可视化数据统计
![](https://github.com/JoyceHxw/Project_KnowledgeGraph/blob/main/distribution_demo.png)
- 智能问答功能
![](https://github.com/JoyceHxw/Project_KnowledgeGraph/blob/main/Q%26A_demo.png)
