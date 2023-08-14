import pandas as pd
import random

companies=pd.read_csv('./data_process/company_processed.csv',usecols=['name'])
shareholders=pd.read_csv('./data_process/shareholder_processed.csv',usecols=['name'])
executives=pd.read_csv('./data_process/executive_processed.csv',usecols=['name'])
industries=pd.read_csv('./data_process/industry_processed.csv',usecols=['name'])
regions=pd.read_csv('./data_process/region_processed.csv',usecols=['name'])

# 整合数据
data = []

for company in companies['name']:
    data.append((f"{company}是一家上市公司。", {"entities": [(0, len(company), "COMPANY")]}))

for shareholder in shareholders['name']:
    data.append((f"{shareholder}是股东。", {"entities": [(0, len(shareholder), "SHAREHOLDER")]}))

for executive in executives['name']:
    data.append((f"{executive}是高管。", {"entities": [(0, len(executive), "EXECUTIVE")]}))

for industry in industries['name']:
    data.append((f"{industry}是一个行业。", {"entities": [(0, len(industry), "INDUSTRY")]}))

for region in regions['name']:
    data.append((f"{region}是一个地区。", {"entities": [(0, len(region), "REGION")]}))


# 随机打乱数据
# random.shuffle(data)