# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import requests
import os
import re
from bs4 import BeautifulSoup

# encoding = 'utf-8'
def getHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Referer": "https://www.mzitu.com/"
        }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    return html


def getSoup(html):
    return BeautifulSoup(html.text, "html.parser")


def main():
    # 请输入你需要爬取的网站模块
    for page in range(2, 186):
        url = 'http://sis001.com/forum/forum-383-'+str(page)+'.html'
        print(url)
        html = getHtml(url)
        soup = getSoup(html)
        # print(soup)
        htmlList = soup.select("tbody >tr>th >span > a")

        for url in htmlList:
            if url.string.isnumeric() == True :
                continue
            else:
                htmltitle = url.string
                htmlurl = 'http://sis001.com/forum/'+url['href']
                makehtml(htmlurl, htmltitle)

def makehtml(url, name):
    # 请输入你需要爬取的网站模块
    # url = 'http://sis001.com/forum/thread-10733299-1-1.html'
    html = getHtml(url)
    soup = getSoup(html)
    htmlList = soup.select("div[style='font-size:14pt']")
    try:
        deleteinfo = [s.extract() for s in htmlList[0](['table', 'strong'])]
    except:
        return
    htmlList = htmlList[0]
    # print(htmlList)
    strhtml = str(htmlList).replace('<br/>', '')


    f = open("%s.txt" % (name), "w", encoding="utf-8")
    try:
        f.write(str(strhtml))
    except:
        print("出错了。。。")
        return
    finally:
        f.close()
    print('正在下载' + name )
if __name__ == '__main__':
    main()
