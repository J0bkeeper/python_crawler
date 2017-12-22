import re
import requests
from requests.exceptions import RequestException
import os
from multiprocessing import Pool
from urllib.parse import urlencode

def get_page(page):
    data = {
        'current_page': page,
        'status': 2,

        # 'legalName':'',
        # 'orgName':'',
        # 'corporateType':'',
        # 'managerDeptCode':'',
        # 'registrationNo':'',
        # 'unifiedCode':'',
        # 'orgAddNo':'',
        # 'ifCharity':'',
        # 'ifCollect':'',
        # 'status':2,
        # 'regNumB':'',
        # 'regNumD':'',
        # 'tabIndex':'',
        # 'regNum':'',
        'page_flag': 'true',
        'pagesize_key': 'macList',
        'goto_page':next,
        # 'current_page': page,
        'total_count': 2315,
        # 'to_page': '',
    }
    print(data.get('current_page'))
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    try:
        url = 'http://www.chinanpo.gov.cn/search/orgcx.html'
        html = requests.post(url,data = data,headers = headers)
        # html.encoding = 'urf-8'
        # print(html)
        if html.status_code == 200:
            return html.text
    except RequestException:
        return None

def parse_page(html):
    pattern = re.compile('href="javascript:toHref\((\d+)\);">(.*?)<.*?align="center" valign="middle">(.*?)<.*?align="center" valign="middle">(.*?)<.*?align="center" valign="middle">(.*?)<.*?align="center" valign="middle">(.*?)<',re.S)
    nums = re.findall(pattern,html)
    for i in nums:
        numbers = i[0]
        # print(numbers)
        detail = []
        for j in i:
            j = j.replace('\\r','').replace('\\t','').replace('\\n','').replace('&nbsp;','').strip()
            detail.append(j)
        data = {
            'orgId': numbers
        }
        headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        url = 'http://www.chinanpo.gov.cn/search/vieworg.html'
        response = requests.post(url,data = data,headers = headers)
        pattern = re.compile('<table width="100%" border="0" align="center" cellpadding="0" cellspacing="1" bgcolor="#cbd9f4" class="mar-top">(.*?)</table',re.S)
        rrr = re.findall(pattern,response.text)
        pattern = re.compile('登记管理机关：.*?align="left">(.*?)<.*?业务主管单位：.*?align="left">(.*?)<.*?注册资金：.*?align="left">(.*?)<.*?联系电话：.*?align="left">(.*?)<.*?社会组织类型：.*?align="left">(.*?)<.*?住    所：.*?colspan="3">(.*?)<',re.S)
        dengji = re.findall(pattern,str(rrr))
        for r in dengji:
            for q in r:
                q = q.replace('\\r','').replace('\\n','').replace('\\t','').replace('&nbsp;','').strip()
                detail.append(q)
        print(detail)

def main(page):
    html = get_page(page)
    # print(html)
    res = parse_page(html)


if __name__ == '__main__':
    page = [page for page in range(1,4)]
    print(page)
    pool = Pool()
    pool.map(main,page)
    pool.close()
    # for i in range(1,3):
    #     main(i)