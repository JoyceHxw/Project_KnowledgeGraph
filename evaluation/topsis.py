'''
    0.数据获取
        涉及指标：盈利能力（平均ROE），市场规模（市值），财务风险（资产负债率），股东实力（股东投资数量），管理水平（任职公司数量）
    1.计算加权的向量规范化属性矩阵：一致化（效益型，成本型，区间型），无量纲化，归一化
        分行业进行
        效益性：盈利能力，市场规模，股东实力，管理水平
        成本型：财务风险，
    2.计算正理想解和负理想解
    3.计算到正负理想解的距离
    4.排序
'''
import pandas as pd
# 0.数据获取------------------------------------------
# 财务数据
def get_finance_data():
    finance_data=pd.read_csv('./data_process/company_finance_processed.csv')
    finance_data[['ROE_2022','ROE_2021','ROE_2020','ROE_2019','ROE_2018','asset_liability_2022','asset_liability_2021','asset_liability_2020','asset_liability_2019','asset_liability_2018']]
    # print(finance_data['ROE_2022'].mean())
    finance_data['ROE_avg']=finance_data[['ROE_2022','ROE_2021','ROE_2020','ROE_2019','ROE_2018']].mean(axis=1)
    finance_data['asset_liability_avg']=finance_data[['asset_liability_2022','asset_liability_2021','asset_liability_2020','asset_liability_2019','asset_liability_2018']].mean(axis=1)
    finance_data=finance_data[['name','ROE_avg','asset_liability_avg']]
    finance_data.to_csv('./evaluation/finance_data_mean.csv',index=False)
# get_finance_data()

# 股东实力
# 股东数量*0.4+股东投资数>=3的股东数量*0.6
from py2neo import Graph
def get_shareholder_data():
    graph=Graph("bolt://localhost:7687", auth=("neo4j", "2214563hxw"))
    query="""
        match (n1:Shareholder)-[r1:INVEST]->(m1:Company)
        with n1,count(m1) as invest_cnt
        where invest_cnt>2
        match (n:Shareholder)-[r:INVEST]->(m:Company)
        with n,m
        where n=n1
        return m.name, count(n) as strong_shareholder_num
        """
    result=graph.run(query)
    shareholder_strong_num=pd.DataFrame(result,columns=['name','strong_shareholder_num'])
    # shareholder_strong_num.to_csv('./evaluation/strong_shareholder_num.csv',index=False)
    query2="""
        match (n:Shareholder)-[r:INVEST]->(m:Company)
        with m, count(n) as shareholder_num
        return m.name,shareholder_num
        """
    result2=graph.run(query2)
    shareholder_num=pd.DataFrame(result2,columns=['name','shareholder_num'])
    shareholder_data=pd.merge(shareholder_num,shareholder_strong_num,on='name',how="left")
    shareholder_data=shareholder_data.fillna(0)
    shareholder_data['shareholder_capacity']=shareholder_data['shareholder_num']*0.4+shareholder_data['strong_shareholder_num']*0.6
    shareholder_data.to_csv('./evaluation/shareholder_data.csv',index=False)
# get_shareholder_data()

# 管理水平
# 高管数量*0.4+高管任职公司数>1的高管数*0.6
def get_executive_data():
    graph=Graph("bolt://localhost:7687", auth=("neo4j", "2214563hxw"))
    query="""
        match (n1:Executive)-[r1:MANAGE]->(m1:Company)
        with n1,count(m1) as position_cnt
        where position_cnt>1
        match (n:Executive)-[r:MANAGE]->(m:Company)
        with n,m
        where n=n1
        return m.name, count(n) as strong_executive_num
        """
    result=graph.run(query)
    strong_executive_num=pd.DataFrame(result,columns=['name','strong_executive_num'])
    strong_executive_num.to_csv('./evaluation/strong_executive_num.csv',index=False)
    query2="""
        match (n:Executive)-[r:MANAGE]->(m:Company)
        with m, count(n) as executive_num
        return m.name,executive_num
        """
    result2=graph.run(query2)
    executive_num=pd.DataFrame(result2,columns=['name','executive_num'])
    executive_data=pd.merge(executive_num,strong_executive_num,on='name',how='left')
    executive_data=executive_data.fillna(0)
    executive_data['management_capacity']=executive_data['executive_num']*0.4+executive_data['strong_executive_num']*0.6
    executive_data.to_csv('./evaluation/executive_data.csv',index=False)
# get_executive_data()

# 合并数据
def merge_data():
    company_basic_data=pd.read_csv('./data_process/company_industry_processed.csv')
    finance_data=pd.read_csv('./evaluation/finance_data_mean.csv')
    shareholder_data=pd.read_csv('./evaluation/shareholder_data.csv')
    executive_data=pd.read_csv('./evaluation/executive_data.csv')
    evaluation_data=pd.merge(company_basic_data,finance_data,on='name',how="inner")
    evaluation_data=pd.merge(evaluation_data,shareholder_data,on='name',how="inner")
    evaluation_data=pd.merge(evaluation_data,executive_data,on="name",how="inner")
    evaluation_data=evaluation_data[['name','industry','market_value','ROE_avg','asset_liability_avg','shareholder_capacity','management_capacity']]
    evaluation_data.to_csv('./evaluation/evaluation_data.csv',index=False)
# merge_data()


# topsis
import numpy as np
from sklearn import preprocessing
def topsis():
    evaluation_data=pd.read_csv('./evaluation/evaluation_data.csv')
    # 分行业
    industry_data=evaluation_data.groupby('industry')
    topsis_result=pd.DataFrame()
    # 权重，市场规模，盈利能力，财务风险，股东实力，管理水平
    weights=np.array([0.25,0.25,0.2,0.1,0.2])
    # 效益型成本型属性
    attributes_type=np.array([1,1,0,1,1])
    for industry, data in industry_data:
        decision_data=data[['market_value','ROE_avg','asset_liability_avg','shareholder_capacity','management_capacity']]
        # print(decision_data)
        # 1.计算加权的向量规范化属性矩阵
        normalized_data=preprocessing.normalize(decision_data,norm='l2',axis=0)
        weighted_normalized_data=normalized_data*weights
        # 2.计算正理想解和负理想解
        ideal_best=np.where(attributes_type==1,np.max(weighted_normalized_data,axis=0),np.min(weighted_normalized_data,axis=0))
        ideal_worst=np.where(attributes_type==1,np.min(weighted_normalized_data,axis=0),np.max(weighted_normalized_data,axis=0))
        # 3.计算到正负理想解的距离
        distance_to_best=np.sqrt(np.sum((weighted_normalized_data-ideal_best)**2,axis=1))
        distance_to_worst=np.sqrt(np.sum((weighted_normalized_data-ideal_worst)**2,axis=1))
        # 4.综合评价指数，排名
        topsis_score=distance_to_worst/(distance_to_worst+distance_to_best)
        rank=len(topsis_score) - np.argsort(topsis_score).argsort()   #argsort返回的是排序后的索引值
        min_score = np.min(topsis_score)
        max_score = np.max(topsis_score)
        data['topsis_score']=np.round(topsis_score*100,2)
        data['topsis_score_percentage']=np.round( (topsis_score - min_score) / (max_score - min_score) * 100,2)
        data['rank']=rank
        data['ROE_avg']=np.round(data['ROE_avg'],2)
        data['asset_liability_avg']=np.round(data['asset_liability_avg'],2)
        data['shareholder_capacity']=np.round(data['shareholder_capacity'],2)
        data['management_capacity']=np.round(data['management_capacity'],2)
        topsis_result=pd.concat([topsis_result,data])
        # print(data)
    # print(topsis_result)
    topsis_result.to_csv('./evaluation/topsis_result.csv',index=False)
topsis()