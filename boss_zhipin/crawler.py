#!/usr/bin/env python3
# coding: utf-8

# version: 0.1


import requests
from lxml import etree
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def get_url():
    page = 1
    while True:
        url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry={page}&position={page}".format(page=page)
        yield url
        page += 1


def parser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    url = get_url()
    while True:
        url_ = next(url)
        res = requests.get(url_, headers=headers)
        res_code = res.status_code()
        if res_code != 200:
            raise SystemExit("Connection Error: "+str(res_code))
        html = etree.HTML(res.content)
        # 职位名称
        job_name = html.xpath('//div[@class="job-title"]/text()')
        # 月薪
        salary = html.xpath('//span[@class="red"]/text()')
        # 公司名称
        company = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/h3[@class="name"]/a/text()')
        # 工作点的(城市)、工作经验、学历
        al = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/p/text()')
        length = len(al)
        company_address = [al[i].split()[0] for i in range(0, len(al), 3)]
        experience = [al[i] for i in range(1, len(al), 3)]
        degree = [al[i] for i in range(2, len(al), 3)]
        # 公司类型、融资、规模（有的公司未填写融资情况，故不好拆分）
        _finance = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/p/text()')
        # # 公司类型
        # company_type = [_finance[i] for i in range(0, len(_finance), 3)]
        # # 融资情况
        # finance = [_finance[i] for i in range(1, len(_finance), 3)]
        # # 公司规模
        # scale = [_finance[i] for i in range(2, len(_finance), 3)]


url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry=1&position=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
res = requests.get(url, headers=headers)
html = etree.HTML(res.content)
job_name = html.xpath('//div[@class="job-title"]/text()')
salary = html.xpath('//span[@class="red"]/text()')
company = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/h3[@class="name"]/a/text()')


al = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/p/text()')
company_address = [al[i].split()[0] for i in range(0, len(al), 3)]
experience = [al[i] for i in range(1, len(al), 3)]
degree = [al[i] for i in range(2, len(al), 3)]

# 公司类型、融资、规模(有的公司未写融资情况)
_finance = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/p/text()')
# 公司类型
# company_type = [_finance[i] for i in range(0, len(_finance), 3)]
# # 融资情况
# finance = [_finance[i] for i in range(1, len(_finance), 3)]
# # 公司规模
# scale = [_finance[i] for i in range(2, len(_finance), 3)]


# 公司具体情况
# c_url = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/h3[@class="name"]/a/@href')
# company_url = ["https://www.zhipin.com"+_ for _ in c_url]
# job_responsibilities = 1


# column_names = ['job_name', 'salary', 'company', 'company_address', 'experience', 'degree']
# with open(r"C:\Users\sxuan\Desktop\boss_zhipin.csv", 'wt', newline='') as f:
#     f_csv = csv.writer(f)
#     f_csv.writerow(column_names)
#     for job in zip(job_name, salary, company, company_address, experience, degree):
#         f_csv.writerow(job)


print(_finance, len(_finance))
print(company_type, len(company_type))
print(finance, len(finance))
print(scale, len(scale))
# print(job_name, len(job_name))
# print(salary, len(salary))
# print(company, len(company))
# print(company_address)
