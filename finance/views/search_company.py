from django.shortcuts import render,HttpResponse
from py2neo import Graph
import json
from mysite import local_settings

# 全局变量，调用Neo4j数据库
graph=Graph(password=local_settings.NEO4j_DATABASES['default']['PASSWORD'])

def search_result_overview(request):
    global graph
    name=request.GET.get('name','')
    # 公司基本信息
    query_basic="""
        match (n:Company) 
        where n.name=$name 
        return n.name,n.id,n.introduction,n.business_scope,n.market_value,n.incorporation_date,n.listing_date,
            n.ROE_2022,n.ROE_2021,n.ROE_2020,n.ROE_2019,n.ROE_2018,n.asset_liability_2022,n.asset_liability_2021,n.asset_liability_2020,n.asset_liability_2019,n.asset_liability_2018,
            n.ROE_avg,n.asset_liability_avg,n.topsis_score,n.rank,n.shareholder_capacity,n.management_capacity,
            n.strong_shareholder_num,n.strong_executive_num,
            n.industry, n.region
        """
    parameters={"name":name}
    company_basic=graph.run(query_basic,parameters).data()
    if company_basic:
        company_basic=company_basic[0]
        company_name=company_basic.get("n.name")
        company_id=company_basic.get("n.id")
        company_introduction=company_basic.get("n.introduction")
        company_business_scope=company_basic.get("n.business_scope")
        company_market_value=company_basic.get("n.market_value")
        company_incorporation_date=company_basic.get("n.incorporation_date")
        company_listing_date=company_basic.get("n.listing_date")
        ROE_2022=company_basic.get("n.ROE_2022")
        ROE_2021=company_basic.get("n.ROE_2021")
        ROE_2020=company_basic.get("n.ROE_2020")
        ROE_2019=company_basic.get("n.ROE_2019")
        ROE_2018=company_basic.get("n.ROE_2018")
        asset_liability_2022=company_basic.get("n.asset_liability_2022")
        asset_liability_2021=company_basic.get("n.asset_liability_2021")
        asset_liability_2020=company_basic.get("n.asset_liability_2020")
        asset_liability_2019=company_basic.get("n.asset_liability_2019")
        asset_liability_2018=company_basic.get("n.asset_liability_2018")
        ROE_avg=company_basic.get("n.ROE_avg")
        asset_liability_avg=company_basic.get("n.asset_liability_avg")
        topsis_score=company_basic.get("n.topsis_score")
        rank=company_basic.get("n.rank")
        shareholder_capacity=company_basic.get("n.shareholder_capacity")
        management_capacity=company_basic.get("n.management_capacity")
        strong_shareholder_num=company_basic.get("n.strong_shareholder_num")
        strong_executive_num=company_basic.get("n.strong_executive_num")
        industry=company_basic.get("n.industry")
        region=company_basic.get("n.region")
    else:
        company_name=None
        company_id=None
        company_introduction=None
        company_business_scope=None
        company_market_value=None
        company_incorporation_date=None
        company_listing_date=None
        ROE_2022=None
        ROE_2021=None
        ROE_2020=None
        ROE_2019=None
        ROE_2018=None
        asset_liability_2022=None
        asset_liability_2021=None
        asset_liability_2020=None
        asset_liability_2019=None
        asset_liability_2018=None
        ROE_avg=None
        asset_liability_avg=None
        topsis_score=None
        rank=None
        shareholder_capacity=None
        management_capacity=None
        strong_shareholder_num=None
        strong_executive_num=None
        industry=None
        region=None

    company_basic_info={
        "company_name":company_name,
        "company_id":company_id,
        "company_introduction":company_introduction,
        "company_business_scope":company_business_scope,
        "company_market_value":company_market_value,
        "company_incorporation_date":company_incorporation_date,
        "company_listing_date":company_listing_date,
        "ROE_2022":ROE_2022,
        "ROE_2021":ROE_2021,
        "ROE_2020":ROE_2020,
        "ROE_2019":ROE_2019,
        "ROE_2018":ROE_2018,
        "asset_liability_2022":asset_liability_2022,
        "asset_liability_2021":asset_liability_2021,
        "asset_liability_2020":asset_liability_2020,
        "asset_liability_2019":asset_liability_2019,
        "asset_liability_2018":asset_liability_2018,
        "ROE_avg":ROE_avg,
        "asset_liability_avg":asset_liability_avg,
        "topsis_score":topsis_score,
        "rank":rank,
        "shareholder_capacity":shareholder_capacity,
        "management_capacity":management_capacity,
        "strong_shareholder_num":strong_shareholder_num,
        "strong_executive_num":strong_executive_num,
        "industry":industry,
        "region":region
    }
    
    # 股东信息
    query_shareholders="""
        match (m:Shareholder)-[r:INVEST]->(n:Company) 
        where n.name=$name
        return m,r,n
        """
    company_shareholders=graph.run(query_shareholders,parameters).data()
    company_shareholders_json=json.dumps(company_shareholders,ensure_ascii=False)

    # 高管信息
    query_executives="""
        match (m:Executive)-[r:MANAGE]->(n:Company) 
        where n.name=$name 
        return m,r,n
        """
    company_executives=graph.run(query_executives,parameters).data()
    company_executives_json=json.dumps(company_executives,ensure_ascii=False)

    # 同行信息
    query_industry="""
        match (n:Company)
        where n.name=$name 
        with n
        match (n1:Company)
        where n1.industry=n.industry
        return n1
        """
    industry_companies=graph.run(query_industry,parameters).data()
    industry_companies_json=json.dumps(industry_companies,ensure_ascii=False)

    # 同行公司个数
    query_industry_num="""
        match (n:Company)
        where n.name=$name 
        with n
        match (n1:Company)
        where n1.industry=n.industry
        return count(n1) as industry_companies_num
        """
    industry_companies_num=graph.run(query_industry_num,parameters).data()[0].get('industry_companies_num')

    company_info={
        "company_basic_info":company_basic_info,
        "company_shareholders_json":company_shareholders_json,
        "company_executives_json":company_executives_json,
        "industry_companies_json":industry_companies_json,
        "industry_companies_num":industry_companies_num,
        "name":name
    }
    return render(request,'company_overview.html',company_info)

def search_result_structure(request):
    global graph
    name=request.GET.get('name','')
    parameters={"name":name}
    # 股东信息
    query_shareholders="""
        match (m:Shareholder)-[r:INVEST]->(n:Company) 
        where n.name=$name
        return m,r,n
        """
    company_shareholders=graph.run(query_shareholders,parameters).data()
    company_shareholders_json=json.dumps(company_shareholders,ensure_ascii=False)

    # 高管信息
    query_executives="""
        match (m:Executive)-[r:MANAGE]->(n:Company) 
        where n.name=$name 
        return m,r,n
        """
    company_executives=graph.run(query_executives,parameters).data()
    company_executives_json=json.dumps(company_executives,ensure_ascii=False)

    company_info={
        "company_shareholders_json":company_shareholders_json,
        "company_executives_json":company_executives_json,
        "name":name
    }
    return render(request,'company_structure.html',company_info)

def search_result_evaluation(request):
    global graph
    name=request.GET.get('name','')
    # 公司基本信息
    query_basic="""
        match (n:Company) 
        where n.name=$name 
        return n.name,n.id,n.introduction,n.business_scope,n.market_value,n.incorporation_date,n.listing_date,
            n.ROE_2022,n.ROE_2021,n.ROE_2020,n.ROE_2019,n.ROE_2018,n.asset_liability_2022,n.asset_liability_2021,n.asset_liability_2020,n.asset_liability_2019,n.asset_liability_2018,
            n.ROE_avg,n.asset_liability_avg,n.topsis_score,n.rank,n.shareholder_capacity,n.management_capacity,
            n.strong_shareholder_num,n.strong_executive_num,
            n.industry, n.region
        """
    parameters={"name":name}
    company_basic=graph.run(query_basic,parameters).data()
    if company_basic:
        company_basic=company_basic[0]
        company_name=company_basic.get("n.name")
        company_id=company_basic.get("n.id")
        company_introduction=company_basic.get("n.introduction")
        company_business_scope=company_basic.get("n.business_scope")
        company_market_value=company_basic.get("n.market_value")
        company_incorporation_date=company_basic.get("n.incorporation_date")
        company_listing_date=company_basic.get("n.listing_date")
        ROE_2022=company_basic.get("n.ROE_2022")
        ROE_2021=company_basic.get("n.ROE_2021")
        ROE_2020=company_basic.get("n.ROE_2020")
        ROE_2019=company_basic.get("n.ROE_2019")
        ROE_2018=company_basic.get("n.ROE_2018")
        asset_liability_2022=company_basic.get("n.asset_liability_2022")
        asset_liability_2021=company_basic.get("n.asset_liability_2021")
        asset_liability_2020=company_basic.get("n.asset_liability_2020")
        asset_liability_2019=company_basic.get("n.asset_liability_2019")
        asset_liability_2018=company_basic.get("n.asset_liability_2018")
        ROE_avg=company_basic.get("n.ROE_avg")
        asset_liability_avg=company_basic.get("n.asset_liability_avg")
        topsis_score=company_basic.get("n.topsis_score")
        rank=company_basic.get("n.rank")
        shareholder_capacity=company_basic.get("n.shareholder_capacity")
        management_capacity=company_basic.get("n.management_capacity")
        strong_shareholder_num=company_basic.get("n.strong_shareholder_num")
        strong_executive_num=company_basic.get("n.strong_executive_num")
        industry=company_basic.get("n.industry")
        region=company_basic.get("n.region")
    else:
        company_name=None
        company_id=None
        company_introduction=None
        company_business_scope=None
        company_market_value=None
        company_incorporation_date=None
        company_listing_date=None
        ROE_2022=None
        ROE_2021=None
        ROE_2020=None
        ROE_2019=None
        ROE_2018=None
        asset_liability_2022=None
        asset_liability_2021=None
        asset_liability_2020=None
        asset_liability_2019=None
        asset_liability_2018=None
        ROE_avg=None
        asset_liability_avg=None
        topsis_score=None
        rank=None
        shareholder_capacity=None
        management_capacity=None
        strong_shareholder_num=None
        strong_executive_num=None
        industry=None
        region=None

    company_basic_info={
        "company_name":company_name,
        "company_id":company_id,
        "company_introduction":company_introduction,
        "company_business_scope":company_business_scope,
        "company_market_value":company_market_value,
        "company_incorporation_date":company_incorporation_date,
        "company_listing_date":company_listing_date,
        "ROE_2022":ROE_2022,
        "ROE_2021":ROE_2021,
        "ROE_2020":ROE_2020,
        "ROE_2019":ROE_2019,
        "ROE_2018":ROE_2018,
        "asset_liability_2022":asset_liability_2022,
        "asset_liability_2021":asset_liability_2021,
        "asset_liability_2020":asset_liability_2020,
        "asset_liability_2019":asset_liability_2019,
        "asset_liability_2018":asset_liability_2018,
        "ROE_avg":ROE_avg,
        "asset_liability_avg":asset_liability_avg,
        "topsis_score":topsis_score,
        "rank":rank,
        "shareholder_capacity":shareholder_capacity,
        "management_capacity":management_capacity,
        "strong_shareholder_num":strong_shareholder_num,
        "strong_executive_num":strong_executive_num,
        "industry":industry,
        "region":region
    }

    # 同行信息
    query_industry="""
        match (n:Company)
        where n.name=$name 
        with n
        match (n1:Company)
        where n1.industry=n.industry
        return n1
        """
    industry_companies=graph.run(query_industry,parameters).data()
    industry_companies_json=json.dumps(industry_companies,ensure_ascii=False)

    # 同行公司个数
    query_industry_num="""
        match (n:Company)
        where n.name=$name 
        with n
        match (n1:Company)
        where n1.industry=n.industry
        return count(n1) as industry_companies_num
        """
    industry_companies_num=graph.run(query_industry_num,parameters).data()[0].get('industry_companies_num')

    company_info={
        "company_basic_info":company_basic_info,
        "industry_companies_json":industry_companies_json,
        "industry_companies_num":industry_companies_num,
        "name":name
    }
    return render(request,'company_evaluation.html',company_info)