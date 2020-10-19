# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import requests
import os
import re
from bs4 import BeautifulSoup
import multiprocessing

# encoding = 'utf-8'
def getHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Referer": "http://sis001.com/"
        }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    return html


def getSoup(html):
    return BeautifulSoup(html.text, "html.parser")


def makehtml(url, name):
    html = getHtml(url)
    soup = getSoup(html)
    htmlList = soup.select("div[style='font-size:14pt']")
    try:
        deleteinfo = [s.extract() for s in htmlList[0](['table', 'strong'])]
    except:
        return
    htmlList = htmlList[0]
    # print(htmlList)
    strhtml = str(htmlList).replace('<br/>', '')[100:]
    # print(strhtml)
    # 保存到txt文件中
    f = open("story/%s.txt" % (name), "w", encoding="utf-8")
    try:
        f.write(str(strhtml))
    except:
        print("出错了。。。")
        return
    finally:
        f.close()
    print('正在下载' + name )


def main(x,y):
    # 请输入你需要爬取的网站模块
    for page in range(x, y):
        url = 'http://sis001.com/forum/forum-383-'+str(page)+'.html'
        print(url)
        html = getHtml(url)
        soup = getSoup(html)
        # print(soup)
        htmlList = soup.select("tbody >tr>th >span > a")


        for url in htmlList:
            if url.string.isnumeric() == True or str(url).find("color: red")!=-1 :
                continue
            else:
                htmltitle = re.sub(r"|[\\/:*?\"<>|]+", "", url.string.strip())
                htmlurl = 'http://sis001.com/forum/'+url['href']
                makehtml(htmlurl, htmltitle)
                # print(url)

if __name__ == '__main__':

    # 创建进程
    begin = 1
    bc = 45  # 步长
    # 每次少50 5570 - 5*10 = 5520
    process_dl0 = multiprocessing.Process(target=main, args=(begin, begin + bc))
    process_dl1 = multiprocessing.Process(target=main, args=(begin + bc, begin + 2 * bc))
    process_dl2 = multiprocessing.Process(target=main, args=(begin + 2 * bc, begin + 3 * bc))
    process_dl3 = multiprocessing.Process(target=main, args=(begin + 3 * bc, begin + 4 * bc))
    process_dl4 = multiprocessing.Process(target=main, args=(begin + 4 * bc, begin + 5 * bc))
    #
    # print("完成")
    # 启动进程
    process_dl0.start()
    process_dl1.start()
    process_dl2.start()
    process_dl3.start()
    process_dl4.start()
