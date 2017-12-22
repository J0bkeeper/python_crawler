import re
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def get_hangye_html():
    url= 'http://www.etlong.com/company/'
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    html = requests.get(url,headers = headers)
    return html.text

def parse_hangye_url(html):
    pattern = re.compile('公司黄页分类.*?class="NavList">(.*?)</div>',re.S)
    res = re.findall(pattern,html)
    pattern = re.compile('href="(.*?)">',re.S)
    urls = re.findall(pattern,str(res))
    return urls

def get_company_url(urls):
    for url in urls:
        qian = url[:-5] + '-'
        wei  = '.html'
        for num in range(1,5):
            url = qian + str(num) + wei
            response = requests.get(url)
            pattern = re.compile('class="proname".*?href="(.*?)".*?target',re.S)
            res = re.findall(pattern,response.text)
            for i in res:
                detail = []
                url = i + 'contact/'
                detail_content = requests.get(url).text
                pattern = re.compile('<td width="100">.*?<td>(.*?)<.*?<td>.*?<td>(.*?)<.*?<td>.*?<td>(.*?)<',re.S)
                res = re.findall(pattern,detail_content)

                for i in res:
                    for j in i:
                        j = j.replace(',','').strip()
                        detail.append(j)
                company_phone = re.compile('<td>公司电话：.*?<td>(.*?)<',re.S)
                ress = re.findall(company_phone,detail_content)
                if ress != []:
                    detail.append(ress[0])

                email = re.compile('<td>电子邮件：.*?<td>(.*?)<',re.S)
                res = re.findall(email,detail_content)
                if res == []:
                    detail.append('')
                else:
                    detail.append(res[0])
                lianxiren = re.compile('<td>联 系 人：.*?<td>(.*?)<', re.S)
                res = re.findall(lianxiren, detail_content)
                if res == []:
                    detail.append('')
                else:
                    detail.append(res[0])
                phone_number = re.compile('<td>手机号码：.*?<td>(.*?)<', re.S)
                res = re.findall(phone_number, detail_content)
                if res == []:
                    detail.append('')
                else:
                    detail.append(res[0])
                with open('1215.csv','a')as f:
                    f.write(str(detail) + '\n')

def main():
    html = get_hangye_html()
    hangye_url = parse_hangye_url(html)
    response = get_company_url(hangye_url)


if __name__ == '__main__':
    main()