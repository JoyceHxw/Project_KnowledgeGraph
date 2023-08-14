
import requests
import csv
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url_json='https://quote.eastmoney.com/center/api/sidemenu.json'
user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

request_headers={
    "User-Agent":user_agent
}



# 公司信息
def get_company(url_str,request_headers,industry_name,csv_writer2,csv_writer3,csv_writer4):
    # session=HTMLSession()
    # resp=session.get(url=url_str,headers=request_headers,timeout=(2,5),verify=False)
    # status_code=resp.status_code
    # if status_code==200:
    #     resp.html.render(sleep=2,retries=3, timeout=20000)
    #     html_txt=resp.html.html  # 动态渲染可能导致数据重复，需要去重
    #     # html_txt=response.text

    # 动态渲染也没用，js信息，用selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get(url_str)

    driver.implicitly_wait(10)

    # 遍历公司
    def find_company_elements():
        company_elements = driver.find_elements(By.CSS_SELECTOR,'#table_wrapper-table > tbody > tr')  
        for company_element in company_elements:
            company_code=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(2) > a').text
            company_name=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(3) > a').text
            company_link=company_element.find_element(By.CSS_SELECTOR,'td:nth-child(3) > a').get_attribute('href')
            if company_code[0] in['6','9']:
                exchange='sh'
            elif company_code[0] in['0','3','2']:
                exchange = 'sz'
            elif company_code[0] in ['4','8']:
                exchange = 'bj'
            company_shareholder_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=',exchange,company_code])
            company_companymgt_link=''.join(['https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=',exchange,company_code])
            # print(company_code,company_name,company_link,company_shareholder_link,company_companymgt_link)
            csv_writer2.writerow((industry_name,company_code,company_name,company_link,company_shareholder_link,company_companymgt_link))
            #调用股东
            get_shareholder(company_shareholder_link,  company_name, csv_writer3)
            #调用高管
            get_companymgt(company_companymgt_link,  company_name, csv_writer4)

    #股东函数
    def get_shareholder(company_shareholder_link, company_name, csv_writer3):
        chrome_options2 = Options()
        chrome_options2.add_argument("--headless")
        chrome_options2.add_argument("--disable-gpu")
        driver2 = webdriver.Chrome(options=chrome_options2)
        driver2.get(company_shareholder_link)
        driver2.implicitly_wait(10)
        shareholer_elements = driver2.find_elements(By.CSS_SELECTOR,'#content_sdgd>table > tbody > tr')
        for shareholer_element in shareholer_elements[1:-1]:
            shareholer_name=shareholer_element.find_element(By.CSS_SELECTOR,'td:nth-child(2) ').text
            shareholer_rate=shareholer_element.find_element(By.CSS_SELECTOR,'td:nth-child(5) ').text
            print(company_name,shareholer_name,shareholer_rate)
            csv_writer3.writerow((company_name,shareholer_name,shareholer_rate))

    #高管函数
    def get_companymgt(company_companymgt_link,  company_name, csv_writer4):
        chrome_options3 = Options()
        chrome_options3.add_argument("--headless")
        chrome_options3.add_argument("--disable-gpu")
        driver3 = webdriver.Chrome(options=chrome_options3)
        driver3.get(company_companymgt_link)
        driver3.implicitly_wait(10)
        companymgt_elements = driver3.find_elements(By.CSS_SELECTOR,'div.section.first>div.content>table > tbody > tr')
        for companymgt_element in companymgt_elements[1:]:
            companymgt_name=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(2) ').text
            companymgt_gender=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(3) ').text
            companymgt_age=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(4) ').text
            companymgt_education=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(5) ').text
            companymgt_pay=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(7) ').text
            companymgt_position=companymgt_element.find_element(By.CSS_SELECTOR,'td:nth-child(8) ').text
            print(company_name,companymgt_name,companymgt_gender,companymgt_age,companymgt_education,companymgt_pay,companymgt_position)
            csv_writer4.writerow((company_name,companymgt_name,companymgt_gender,companymgt_age,companymgt_education,companymgt_pay,companymgt_position))

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
                find_company_elements()
        except:
            break

    driver.quit()


        
# 行业信息
def get_industry(url_json,request_headers):
    response=requests.get(url=url_json,headers=request_headers)
    status_code=response.status_code

    # 行业信息表
    fp=open('./industry_info.csv',"w",newline="",encoding="utf-8")
    csv_writer=csv.writer(fp)
    csv_header_info=("行业名称","行业链接",)
    csv_writer.writerow(csv_header_info)

    # 行业公司对照表
    fp2=open('./company_industry_info.csv',"w",newline="",encoding="utf-8")
    csv_writer2=csv.writer(fp2)
    csv_header_info2=("行业名称","公司代码","公司名称","公司链接","公司股东页面链接","公司高管页面链接")
    csv_writer2.writerow(csv_header_info2)

    #股东表
    fp3 = open('./shareholder_info.csv', "w", newline="", encoding="utf-8")
    csv_writer3 = csv.writer(fp3)
    csv_header_info3 = ("公司名称", "股东名称","持股比例",)
    csv_writer3.writerow(csv_header_info3)

    #高管表
    fp4 = open('./companymgt_info.csv', "w", newline="", encoding="utf-8")
    csv_writer4 = csv.writer(fp4)
    csv_header_info4 = ("公司名称","高管姓名", "高管性别", "高管年龄","高管学历","高管薪酬","高管职务")
    csv_writer4.writerow(csv_header_info4)

    if status_code==200:
        data=response.json()
        element_info=data[5]['next'][2]['next']
        for element in element_info:
            industry_name=element['title']
            industry_link='https://quote.eastmoney.com'+element['href']
            csv_writer.writerow((industry_name,industry_link))

            # 调用公司信息函数
            get_company(industry_link,request_headers,industry_name,csv_writer2,csv_writer3,csv_writer4)

    fp.close()

# get_company('https://quote.eastmoney.com/center/boardlist.html#boards2-90.BK0473',request_headers)
get_industry(url_json,request_headers)