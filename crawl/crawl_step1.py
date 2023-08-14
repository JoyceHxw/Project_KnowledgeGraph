
import requests
import csv
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

url_json='https://quote.eastmoney.com/center/api/sidemenu.json'
user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

request_headers={
    "User-Agent":user_agent
}



# 公司信息
def get_company(url_str,request_headers,industry_name,csv_writer2):
    # 动态渲染也没用，js信息，用selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get(url_str)

    driver.implicitly_wait(10)

    # 点击市值
    marketvalue_element=driver.find_element(By.CSS_SELECTOR,'#custom-fields > option:nth-child(3)')
    marketvalue_element.click()
    time.sleep(2)

    # 遍历公司
    def find_company_elements():
        company_elements = driver.find_elements(By.CSS_SELECTOR,'#table_wrapper-table > tbody > tr')  
        for company_element in company_elements:
            company_code=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(2) > a').text
            company_name=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(3) > a').text
            company_link=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(3) > a').get_attribute('href')
            company_marketvalue=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(17)').text
            if company_code[0] in ['6','9']:
                exchange='sh'
            elif company_code[0] in ['0','3','2']:
                exchange='sz'
            elif company_code[0] in ['4','8']:
                exchange='bj'
            company_shareholder_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=',exchange,company_code])
            company_companymgt_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=',exchange,company_code])
            company_finance_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=',exchange,company_code])
            company_overview_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index?type=web&code=',exchange,company_code])
            # print(company_code,company_name,company_link,company_shareholder_link,company_companymgt_link)
            csv_writer2.writerow((industry_name,company_code,company_name,company_link,company_marketvalue,company_shareholder_link,company_companymgt_link,company_finance_link,company_overview_link))

    # 先调用一次
    find_company_elements()

    # 存在分页的情况
    while True:
        try:
            nextpage_element=driver.find_element(By.CSS_SELECTOR,'#main-table_paginate > a.next.paginate_button')
            # 点击下一页
            if 'disable' in nextpage_element.get_attribute('class'):
                break
            else:
                # 点击下一页后再遍历当前页面公司
                nextpage_element.click()
                # driver.implicitly_wait(5)
                time.sleep(5)
                find_company_elements()
        except:
            break

    driver.quit()


        
# 行业信息
def get_industry(url_json,request_headers):
    response=requests.get(url=url_json,headers=request_headers)
    status_code=response.status_code

    # 行业信息表
    fp=open('./crawl/industry_info.csv',"w",newline="",encoding="utf-8")
    csv_writer=csv.writer(fp)
    csv_header_info=("行业名称","行业链接")
    csv_writer.writerow(csv_header_info)

    # 行业公司对照表
    fp2=open('./crawl/company_industry_info.csv',"w",newline="",encoding="utf-8")
    csv_writer2=csv.writer(fp2)
    csv_header_info2=("行业名称","公司代码","公司名称","公司链接","公司市值","公司股东页面链接","公司高管页面链接","公司财务页面链接","公司概况页面链接")
    csv_writer2.writerow(csv_header_info2)

    if status_code==200:
        data=response.json()
        element_info=data[5]['next'][2]['next']
        for element in element_info:
            industry_name=element['title']
            industry_link='https://quote.eastmoney.com'+element['href']
            csv_writer.writerow((industry_name,industry_link))

            # 调用公司信息函数
            get_company(industry_link,request_headers,industry_name,csv_writer2)

    fp.close()
    fp2.close()

# get_company('https://quote.eastmoney.com/center/boardlist.html#boards2-90.BK0473',request_headers)
get_industry(url_json,request_headers)