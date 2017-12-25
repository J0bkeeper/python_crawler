import re
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import os
import time

url_lists = []
def present_time():
    t = time.strftime('%Y-%m-%d', time.localtime())
    return t

def get_index_html(url):
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    html = requests.get(url,headers = headers)
    return html.text

def parse_page(html):
    pattern = re.compile('style="display: block; width: 140px.*?href="(.*?)".*?id',re.S)
    urls = re.findall(pattern,html)
    return urls

def get_detail(t,urls):
    global n
    for i in urls:
        dd = '__' + str(n) + '__'
        # print(i)
        headurl = 'http://www.ashghal.gov.qa'
        reurl = headurl + i
        detailpage = get_index_html(reurl)
        # print(detailpage)
        pattern = re.compile('lblTenderTitleValue">(.*?)<.*?lblTenderNumberValue">(.*?)<.*?lblTenderTypeValue">(.*?)<.*?lblTenderParticipantsValue">(.*?)<.*?lblTenderCategoryValue">(.*?)<.*?lblTenderIssuingDateValue">(.*?)<.*?lblTenderCloseDateValue">(.*?)<.*?',re.S)

        res = re.findall(pattern,detailpage)
        print(res)
        for i in res:
            name = i[1].replace('/','')
            lists = []
            titlele = i[0].replace(',','').replace('&nbsp;','')
            if len(titlele) >35:
                titlele = titlele[:30]
            else:
                titlele = titlele
            for j in i:
                j = j.replace(',','').replace('&nbsp;','')
                lists.append(j)
            aa = str(lists)
            print(aa)
            with open('ashghalgov.csv','a')as f:
                f.write(dd + aa + '\n')
        # filename = titlele + '.pdf'
        pattern1 = re.compile('&quot;&quot;, &quot;(.*?)&quot',re.S)
        ress = re.findall(pattern1,detailpage)
        weiba = str((ress[-2:-1])[0])
        weiba = weiba.replace('\\','')
        resurl = headurl + weiba
        filename = resurl.replace('/','').replace(',','').strip()
        if len(resurl)>=60:
            filename = filename[-55:]
        else:
            filename = filename

        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        response = requests.post(resurl,headers=headers)
        print(resurl)
        print(response.status_code)
        try:
            os.makedirs('{}/{}{}'.format(t,dd,name))
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        except RequestException:
            return None
        with open('{}/{}{}/{}'.format(t,dd,name,filename),'wb')as f:
            f.write(response.content)
        n += 1

def main():
    t = present_time()
    url = 'http://www.ashghal.gov.qa/en/Tenders/pages/DetailedTenderListPage.aspx?Status=Opened'
    html = get_index_html(url)
    urls = parse_page(html)
    detail_page = get_detail(t,urls)
    # print(html)

if __name__ == "__main__":
    n = 1
    main()