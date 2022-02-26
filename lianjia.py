# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import pandas
import time

def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        print("未能获取")

def getDetail(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.info.clear')
    try:
        for item in info:
            address = item.select('.address')[0].get_text().split('|'),
            local = address[0]
            flood = item.select('.flood')[0].get_text().split('-')
            unitPrice = item.select('.unitPrice')[0].get_text()
            yield {
                'title': item.select('.title')[0].get_text(),
                'address-a': local[0],
                'address-b': local[1],
                'address-c(平米)': float(local[1][:-3]),
                'address-d': local[3],
                'address-e': local[4],
                'flood-1': flood[0],
                'flood-2': flood[1],
                'followInfo': item.select('.followInfo')[0].get_text(),
                'totalPrice(万)': float(item.select('.totalPrice')[0].get_text().rstrip('万')),
                'unitPrice（元/平米）': float(re.search('(\d+)', unitPrice, re.S).group(1))
            }
    except:
        print("细节无返回")


if __name__ == '__main__':
    # url = 'https://wh.lianjia.com/ershoufang/'
    # html = getHtml(url)
    # total = re.search('totalPage":(.*?),', html, re.S)
    # page_total = int(total.group(1))
    # print("总页码数 = " + str(page_total))
    l = []
    base_url = 'https://wh.lianjia.com/ershoufang/pg'
    for num in range(1, 2):
        html = getHtml(base_url + str(num))
        detail = getDetail(html)
        for i in detail:
            l.append(i)
        # time.sleep(10)
    df = pandas.DataFrame(l)
    df.to_excel('result.xlsx')
