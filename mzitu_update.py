# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import requests
import os
import multiprocessing
from bs4 import BeautifulSoup
import time
# https://www.mzitu.com/best/ 下载这个模块的所有图片
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


def getTitle(soup):
    title = soup.title.contents[0]
    # '_'所在的索引位置
    number = title.index(' ')
    title = title[:number]

    return str(title)


def getAllPage(soup):
    allPage = soup.select('.pagenavi > a > span')[-2].string
    return allPage

def getdefurl(soup):
    defurl = soup.select(".main-image > p > a > img ")[0].attrs['src'][0:-6]
    return defurl

def makedir(title):
    try:
        os.mkdir(title)
    except:
        print(f"{title} 该文件夹无法被创建，格式有误，已重新创建新的：默认文件夹")
        try:
            os.mkdir("默认文件夹")
            return
        except:
            print("已经存在默认文件夹，跳过创建默认文件夹步骤")
            return
# https://i3.mmzztt.com/2020/06/08a   https://i3.mmzztt.com/2020/06/08a01.jpg
def downloadPic(title, allPage, defurl):
    for number in range(1, int(allPage) + 1):
        picUrl = f"{defurl}{str(number).rjust(2, '0')}.jpg"
        pic = getHtml(picUrl)
        with open(f"{title}/{number}.jpg", "wb+") as f:
            f.write(pic.content)
            print(f"第{number}张图片，正在下载中...")

def index(i,t):
    if i ==0:
        htmllist = t
    elif i == 1:
        htmllist = t
    elif i == 2:
        htmllist = t
    elif i == 3:
        htmllist = t
    else:
        htmllist = t

    for url in htmllist:
        htmlMark = url
        print(htmlMark)
        try:
            html = getHtml(f"{htmlMark}")
            soup = getSoup(html)
            title = getTitle(soup)
            allPage = getAllPage(soup)
            defurl = getdefurl(soup)
            new_title = title
            #new_title = title + htmlMark
            print(new_title)
            makedir(new_title)
        except:
            print("%s网页出现了错误" % htmlMark)
            continue
        downloadPic(new_title, allPage, defurl)
        time.sleep(0.5)




if __name__ == '__main__':

    # 请输入你需要爬取的网站模块
    url = 'https://www.mzitu.com/best/'
    html = getHtml(url)
    soup = getSoup(html)
    htmlList = soup.select(".postlist > ul > li > a")

    htmlListall = []
    for url in htmlList:
        a = url['href']
        htmlListall.append(a)
    print(htmlListall)  # 当前页面所有图片连接的合集

    # 定义多个列表
    htmllist0 = []
    htmllist1 = []
    htmllist2 = []
    htmllist3 = []
    htmllist4 = []
    for i in range(len(htmlListall)):
        if i % 5 == 0:
            htmllist0.append(htmlListall[i])
        elif i % 5 == 1:
            htmllist1.append(htmlListall[i])
        elif i % 5 == 2:
            htmllist2.append(htmlListall[i])
        elif i % 5 == 3:
            htmllist3.append(htmlListall[i])
        else:
            htmllist4.append(htmlListall[i])
    htmllist0 = tuple(htmllist0)
    htmllist1 = tuple(htmllist1)
    htmllist2 = tuple(htmllist2)
    htmllist3 = tuple(htmllist3)
    htmllist4 = tuple(htmllist4)
    print(htmllist0)
    print(htmllist1)
    print(htmllist2)
    print(htmllist3)
    print(htmllist4)

    # 创建进程
    process_dl0 = multiprocessing.Process(target=index, args=(0,htmllist0))
    process_dl1 = multiprocessing.Process(target=index, args=(1,htmllist1))
    process_dl2 = multiprocessing.Process(target=index, args=(2,htmllist2))
    process_dl3 = multiprocessing.Process(target=index, args=(3,htmllist3))
    process_dl4 = multiprocessing.Process(target=index, args=(4,htmllist4))
    #
    # print("完成")
    # 启动进程
    process_dl0.start()
    process_dl1.start()
    process_dl2.start()
    process_dl3.start()
    process_dl4.start()
