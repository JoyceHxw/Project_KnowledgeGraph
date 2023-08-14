
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd



def get_company_finance():    
    # fp=open('./crawl/company_finance.csv',"w",newline="",encoding="utf-8")
    fp=open('./crawl/company_finance12.csv',"w",newline="",encoding="utf-8")
    csv_writer=csv.writer(fp)
    csv_header_info=("公司代码","公司名称","2022年ROE","2021年ROE","2020年ROE","2019年ROE","2018年ROE","2022年资产负债率","2021年资产负债率","2020年资产负债率","2019年资产负债率","2018年资产负债率")
    csv_writer.writerow(csv_header_info)    

    data=pd.read_csv('./crawl/company_industry_info.csv',usecols=['公司代码','公司名称','公司财务页面链接'])
    
    for index, row in data.iterrows():
        if index>5055:
            company_code = row['公司代码']
            company_name = row['公司名称']
            url_str = row['公司财务页面链接']

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=chrome_options) 
            driver.get(url_str)
            driver.implicitly_wait(10)

            # 点击按年度
            annual_element=driver.find_element(By.CSS_SELECTOR,'#zyzbTab > li:nth-child(2)')
            annual_element.click()
            time.sleep(3)
            i=15
            while i<40:
                ROE_element=driver.find_element(By.CSS_SELECTOR,f'#report_zyzb > table > tbody > tr:nth-child({i})').text
                if "净资产收益率(加权)(%)" in ROE_element:
                    break
                i+=1
            while i<40:
                asset_liability_element=driver.find_element(By.CSS_SELECTOR,f'#report_zyzb > table > tbody > tr:nth-child({i})').text
                if "资产负债率(%)" in asset_liability_element:
                    break
                i+=1

            ROE_list=ROE_element.split(' ')
            asset_liability_list=asset_liability_element.split(' ')
            ROE_2022=ROE_list[1] if len(ROE_list)>=2 else ""
            ROE_2021=ROE_list[2] if len(ROE_list)>=3 else ""
            ROE_2020=ROE_list[3] if len(ROE_list)>=4 else ""
            ROE_2019=ROE_list[4] if len(ROE_list)>=5 else ""
            ROE_2018=ROE_list[5] if len(ROE_list)>=6 else ""
            asset_liability_2022=asset_liability_list[1] if len(asset_liability_list)>=2 else ""
            asset_liability_2021=asset_liability_list[2] if len(asset_liability_list)>=3 else ""
            asset_liability_2020=asset_liability_list[3] if len(asset_liability_list)>=4 else ""
            asset_liability_2019=asset_liability_list[4] if len(asset_liability_list)>=5 else ""
            asset_liability_2018=asset_liability_list[5] if len(asset_liability_list)>=6 else ""

            csv_writer.writerow((company_code,company_name,ROE_2022,ROE_2021,ROE_2020,ROE_2019,ROE_2018,asset_liability_2022,asset_liability_2021,asset_liability_2020,asset_liability_2019,asset_liability_2018))
    fp.close()

get_company_finance()      
