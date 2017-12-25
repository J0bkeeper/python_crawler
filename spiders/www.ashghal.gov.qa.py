import re
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
url_lists = []

def get_index_html(url):
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    html = requests.get(url,headers = headers)
    return html.text

def parse_page(html):
    pattern = re.compile('style="display: block; width: 140px.*?href="(.*?)".*?id',re.S)
    urls = re.findall(pattern,html)
    return urls

def get_detail(urls):
    for i in urls:
        # print(i)
        headurl = 'http://www.ashghal.gov.qa'
        reurl = headurl + i
        detailpage = get_index_html(reurl)
        # print(detailpage)
        pattern = re.compile('lblTenderTitleValue">(.*?)<.*?lblTenderNumberValue">(.*?)<.*?lblTenderTypeValue">(.*?)<.*?lblTenderParticipantsValue">(.*?)<.*?lblTenderCategoryValue">(.*?)<.*?lblTenderIssuingDateValue">(.*?)<.*?lblTenderCloseDateValue">(.*?)<.*?',re.S)

        res = re.findall(pattern,detailpage)
        # print(res)
        for i in res:
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
            # print(aa)
            # with open('ashghalgov.csv','a')as f:
            #     f.write(aa + '\n')
        # filename = titlele + '.pdf'
        pattern1 = re.compile('&quot;&quot;, &quot;(.*?)&quot',re.S)
        ress = re.findall(pattern1,detailpage)
        # print(ress)
        weiba = str((ress[-2:-1])[0])
        weiba = weiba.replace('\\','')
        resurl = headurl + weiba
        # resurl = r"{}{}".format(headurl,weiba)

        print(resurl)
        # first = resurl[:58]
        late = resurl[58:]
        filename = late
        # # print(late)
        # url = first + late
        # print(url)
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        response = requests.post(resurl,headers=headers)
        print(resurl)
        print(response.status_code)
        with open(filename,'wb')as f:
            f.write(response.content)

def main():
    url = 'http://www.ashghal.gov.qa/en/Tenders/pages/DetailedTenderListPage.aspx?Status=Opened'
    html = get_index_html(url)
    urls = parse_page(html)
    detail_page = get_detail(urls)
    # print(html)

if __name__ == "__main__":
    main()