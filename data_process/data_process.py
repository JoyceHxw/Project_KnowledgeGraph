import pandas as pd
import numpy as np


# 拼接财务数据
def finance_concat():
    finance_concat0=pd.read_csv('./crawl/company_finance0.csv')
    finance_concat1=pd.read_csv('./crawl/company_finance1.csv')
    finance_concat2=pd.read_csv('./crawl/company_finance2.csv')
    finance_concat3=pd.read_csv('./crawl/company_finance3.csv')
    finance_concat4=pd.read_csv('./crawl/company_finance4.csv')
    finance_concat5=pd.read_csv('./crawl/company_finance5.csv')
    finance_concat6=pd.read_csv('./crawl/company_finance6.csv')
    finance_concat7=pd.read_csv('./crawl/company_finance7.csv')
    finance_concat8=pd.read_csv('./crawl/company_finance8.csv')
    finance_concat9=pd.read_csv('./crawl/company_finance9.csv')
    finance_concat10=pd.read_csv('./crawl/company_finance10.csv')
    finance_concat11=pd.read_csv('./crawl/company_finance11.csv')
    finance_concat12=pd.read_csv('./crawl/company_finance12.csv')
    company_finance=pd.concat([finance_concat0,finance_concat1,finance_concat2,finance_concat3,finance_concat4,finance_concat5,
                           finance_concat6,finance_concat7,finance_concat8,finance_concat9,finance_concat10,finance_concat11,finance_concat12])
    # print(company_finance)
    company_finance.to_csv('./crawl/company_finance.csv',index=False)
# finance_concat()

# 财务表去重
# 信息缺失
# 转换数据格式
def finance_process():
    finance=pd.read_csv('./crawl/company_finance.csv')
    finance.rename(columns={'公司代码':'id','公司名称':'name',
                            "2022年ROE":"ROE_2022",
                            "2021年ROE":"ROE_2021",
                            "2020年ROE":"ROE_2020",
                            "2019年ROE":"ROE_2019",
                            "2018年ROE":"ROE_2018",
                            "2022年资产负债率":"asset_liability_2022",
                            "2021年资产负债率":"asset_liability_2021",
                            "2020年资产负债率":"asset_liability_2020",
                            "2019年资产负债率":"asset_liability_2019",
                            "2018年资产负债率":"asset_liability_2018"},inplace=True)
    finance_deduplicate=finance.drop_duplicates()
    finance_deduplicate.replace('--',np.nan,inplace=True)
    finance_deduplicate[['ROE_2022','ROE_2021','ROE_2020','ROE_2019','ROE_2018','asset_liability_2022','asset_liability_2021','asset_liability_2020','asset_liability_2019','asset_liability_2018']]\
        = finance_deduplicate[['ROE_2022','ROE_2021','ROE_2020','ROE_2019','ROE_2018','asset_liability_2022','asset_liability_2021','asset_liability_2020','asset_liability_2019','asset_liability_2018']].astype(float)
    finance_deduplicate=finance.drop_duplicates()
    finance_deduplicate.replace('--',np.nan,inplace=True)
    finance_deduplicate.to_csv('./data_process/company_finance_processed.csv',index=False)
finance_process()



# 公司地区表去除“板块”
def company_region_process():
    company_region=pd.read_csv('./crawl/company_region_info.csv')
    company_region.rename(columns={'地域名称':'region','公司代码':'id','公司名称':'name'},inplace=True)
    company_region['region'] = company_region['region'].str.replace('板块', '')
    company_region.to_csv('./data_process/company_region_processed.csv',index=False)
# company_region_process()

# 公司行业表
# 提取信息，去除“亿”
def company_industry_process():
    company_industry=pd.read_csv('./crawl/company_industry_info.csv',usecols=['公司代码','公司名称','公司市值','行业名称'])
    company_industry.rename(columns={'公司代码':'id','公司名称':'name','公司市值':'market_value','行业名称':'industry'},inplace=True)
    company_industry['market_value']=company_industry['market_value'].str.replace('亿','').astype(float)
    company_industry.to_csv('./data_process/company_industry_processed.csv',index=False)
# company_industry_process()

# 拼接概况数据
def company_overview_concat():
    overview_concat0=pd.read_csv('./crawl/overview_info0.csv')
    overview_concat1=pd.read_csv('./crawl/overview_info1.csv')
    overview_info=pd.concat([overview_concat0,overview_concat1])
    overview_info.to_csv('./crawl/overview_info.csv',index=False)
# company_overview_concat()

# 公司概况去重
# 替换空值
# 日期格式转换
def company_overview_process():
    overview=pd.read_csv('./crawl/overview_info.csv')
    overview.rename(columns={'公司名称':'name','公司代码':'id','公司简介':'introduction','经营范围':'business_scope','成立日期':'incorporation_date','上市日期':'listing_date'},inplace=True)
    overview.replace('--',np.nan,inplace=True)
    overview['incorporation_date']=pd.to_datetime(overview['incorporation_date'])
    overview['listing_date']=pd.to_datetime(overview['listing_date'])
    overview_deduplicate=overview.drop_duplicates()
    overview_deduplicate.to_csv('./data_process/company_overview_processed.csv',index=False)
# company_overview_process()

# 关联得到公司表
def company_process():
    company_industry=pd.read_csv('./data_process/company_industry_processed.csv')
    company_region=pd.read_csv('./data_process/company_region_processed.csv')
    company_overview=pd.read_csv('./data_process/company_overview_processed.csv')
    company_merge1=pd.merge(company_industry,company_region, on='id',how='inner')
    company_merge2=pd.merge(company_merge1,company_overview,on='id',how='inner')
    company=company_merge2[['id','name_x','industry','region','market_value','incorporation_date','listing_date','introduction','business_scope']]
    company.rename(columns={'name_x':'name'},inplace=True)
    company.to_csv('./data_process/company_processed.csv',index=False)   
# company_process()



# 合并高管表
def companymgt_concat():
    companymgt_concat0=pd.read_csv('./crawl/companymgt_info0.csv')
    companymgt_concat1=pd.read_csv('./crawl/companymgt_info1.csv')
    companymgt_info=pd.concat([companymgt_concat0,companymgt_concat1])
    companymgt_info.to_csv('./crawl/companymgt_info.csv',index=False)
# companymgt_concat()

# 高管公司关系表
# 去重
# 高管信息缺失，替换空值
# 薪酬去除万,格式转换
def companymgt_company_process():
    companymgt=pd.read_csv('./crawl/companymgt_info.csv',usecols=['高管姓名','高管性别','高管年龄','高管学历','高管薪酬','高管职务','公司名称'])
    companymgt.rename(columns={'高管姓名': 'name','高管性别':'gender','高管年龄':'age','高管学历':'education','高管薪酬': 'salary','高管职务':'position','公司名称':'company_name'}, inplace=True)
    companymgt_deduplicate=companymgt.drop_duplicates()
    # print(companymgt_deduplicate)
    companymgt_deduplicate.replace('--',np.nan,inplace=True)
    companymgt_deduplicate['salary'] = companymgt_deduplicate['salary'].str.replace('万', '').astype(float)
    companymgt_deduplicate.to_csv('./data_process/executive_company_processed.csv',index=False)
# companymgt_company_process()

# 高管表
def companymgt_process():
    companymgt=pd.read_csv('./crawl/companymgt_info.csv',usecols=['高管姓名','高管性别','高管年龄','高管学历'])
    companymgt.rename(columns={'高管姓名': 'name','高管性别':'gender','高管年龄':'age','高管学历':'education'}, inplace=True)
    companymgt_deduplicate=companymgt.drop_duplicates()
    # print(companymgt_deduplicate)
    companymgt_deduplicate.replace('--',np.nan,inplace=True)
    companymgt_deduplicate.to_csv('./data_process/executive_processed.csv',index=False)
# companymgt_process()



# 合并股东表
def shareholder_concat():
    shareholder_concat0=pd.read_csv('./crawl/shareholder_info0.csv')
    shareholder_concat1=pd.read_csv('./crawl/shareholder_info1.csv')
    shareholder_info=pd.concat([shareholder_concat0,shareholder_concat1])
    shareholder_info.to_csv('./crawl/shareholder_info.csv',index=False)
# shareholder_concat()

# 股东公司关系表
# 去重
# 持股比例去除%
def shareholder_company_process():
    shareholders_company=pd.read_csv('./crawl/shareholder_info.csv',usecols=['股东名称','持股比例','公司名称'])
    shareholders_company.rename(columns={'股东名称':'name','持股比例':'rate','公司名称':'company_name'},inplace=True)
    shareholders_deduplicate=shareholders_company.drop_duplicates()
    shareholders_deduplicate['rate'] = shareholders_deduplicate['rate'].str.replace('%', '').astype(float)
    shareholders_deduplicate.to_csv('./data_process/shareholder_company_processed.csv',index=False)
# shareholder_company_process()

# 股东表
def shareholder_process():
    shareholders=pd.read_csv('./crawl/shareholder_info.csv',usecols=['股东名称'])
    shareholders.rename(columns={'股东名称':'name'},inplace=True)
    shareholders_deduplicate=shareholders.drop_duplicates()
    shareholders_deduplicate.to_csv('./data_process/shareholder_processed.csv',index=False)
# shareholder_process()



# 行业表
def industry_process():
    industry=pd.read_csv('./crawl/industry_info.csv',usecols=['行业名称'])
    industry.rename(columns={'行业名称':'name'},inplace=True)
    industry.to_csv('./data_process/industry_processed.csv',index=False)
# industry_process()



# 地区表
def region_process():
    region=pd.read_csv('./crawl/company_region_info.csv',usecols=['地域名称'])
    region.rename(columns={'地域名称':'name'},inplace=True)
    region['name'] = region['name'].str.replace('板块', '')
    region_unique=region.drop_duplicates()
    region_unique.to_csv('./data_process/region_processed.csv',index=False)
# region_process()
