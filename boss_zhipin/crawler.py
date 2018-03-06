#!/usr/bin/env python3
# coding: utf-8

# version: 0.2

'''
目前问题：
    融资那里有的公司写了三项（公司类型、融资、规模），有的公司只写了其中两项或一项，考虑如何进行拆分？

更远的要求：
    改进代码：使用协程or多线程or多进程
'''


import requests
from lxml import etree
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def get_page_url():
    '''generate job pages for bioinformatics engineer.'''
    page = 1
    while True:
        url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry={page}&position={page}".format(page=page)
        yield url
        page += 1


def get_res(url):
    '''return the etree.HTML(...) for xpath to extract elements'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # get all job pages for bioinformatics
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise SystemExit("Connection/HTTP Error: "+str(res.status_code))
    html = etree.HTML(res.content)
    return html


def job_skills(comp_url):
    '''get the skills requested by the job, such as perl, python, linux...
       then representing these skills with binary code 1,2,4...
       linux=1, perl=2, python=4, R=8, C++=16, C=32, matlab=64
    '''
    skills_code = {'linux': 1, 'Linux': 1, 'perl': 2, 'Perl': 2, 'python': 4, 'Python': 4,
                   'R': 8, 'C++': 16, 'c++': 16, 'C': 32, 'c': 32, 'matlab': 64, 'Matlab': 64,
                   'mysql': 128, 'Mysql': 128, 'Docker': 256, 'docker': 256}
    skills = []
    for url_ in comp_url:
        code = 0
        html = get_res(url_)
        job_description = html.xpath('//div[@class="job-detail"]/div[@class="detail-content"]/div[@class="job-sec"]/div[@class="text"]/text()')
        content = "".join(job_description)
        for skill in skills_code:
            if skill in content:
                code += skills_code[skill]
        skills.append(code)
    return skills


def parse_html():
    '''parse each page html to get detail content about every job.'''
    page_list = get_page_url()
    for page in page_list:
        html = get_res(page)
        # 职位名称
        job_name = html.xpath('//div[@class="job-title"]/text()')
        # 月薪
        salary = html.xpath('//span[@class="red"]/text()')
        # 公司名称
        company = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/h3[@class="name"]/a/text()')
        # 工作点的(城市)、工作经验、学历
        al = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/p/text()')
        company_address = [al[i].split()[0] for i in range(0, len(al), 3)]
        experience = [al[i] for i in range(1, len(al), 3)]
        degree = [al[i] for i in range(2, len(al), 3)]
        # 公司类型、融资、规模（有的公司未填写融资情况，故不好拆分）
        finance = html.xpath('//div[@class="info-company"]/div[@class="company-text"]/p/text()')
        # # 公司类型
        # company_type = [_finance[i] for i in range(0, len(_finance), 3)]
        # # 融资情况
        # finance = [_finance[i] for i in range(1, len(_finance), 3)]
        # # 公司规模
        # scale = [_finance[i] for i in range(2, len(_finance), 3)]
        ############################################################
        # homepage url of company
        c_url = html.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/h3[@class="name"]/a/@href')
        company_url = ["https://www.zhipin.com"+_ for _ in c_url]
        skills_request = job_skills(company_url)
        yield job_name, salary, company, company_address, experience, degree, finance, skills_request


def write_to_csv():
    column_names = ['job_name', 'salary', 'company', 'company_address', 'experience', 'degree', 'finance', 'skills_request']
    # column_names = ['工作名称', '月薪', '公司', '公司地址', '工作经验', '学历', '融资情况', '职位技能要求']
    with open(r"C:\Users\sxuan\Desktop\boss_zhipin.csv", 'wt', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(column_names)
        job_detail = parse_html()
        for record in job_detail:
            f_csv.writerow(record)


url = "https://www.zhipin.com/job_detail/?query=生物信息分析&scity=100010000&industry=1&position=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
res = requests.get(url, headers=headers)
html = etree.HTML(res.content)

write_to_csv()
