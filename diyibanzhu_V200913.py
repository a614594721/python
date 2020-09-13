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
        "Referer": "https://m.sinodan.cc/"
        }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    return html


def getSoup(html):
    return BeautifulSoup(html.text, "html.parser")

def getmenu(soup):
    menu = soup.find_all('h1')
    result = [a.get_text() for a in menu]
    result = ''.join(result)
    new_title = re.sub(r"|[\\/:*?\"<>| ]+", "", result)
    return new_title


def getList(soup):
    htmlList = soup.select("div >.bd> ul >li > a ")
    htmlList = sorted(set(htmlList), key=htmlList.index)  # sorted output
    # print(htmlList)
    # 去掉htmlList列表中包含'target="_blank"' 的列
    del_results = []

    for i in range(0, len(htmlList)):
        if str(htmlList[i]).find('image') != -1:
            del_results.append(htmlList[i])

    # 用remove() 方法删除列表del_results 表中的元素
    for i in range(0, len(del_results)):
        htmlList.remove(del_results[i])
    return htmlList

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

def order_by(htmlList):
    if len(htmlList)>2:
        l1 = htmlList
        list0 = l1[0]
        list1 = l1[1]
        list2 = l1[2]
        del l1[2]
        l1.append(list2)
        del l1[1]
        l1.append(list1)
        del l1[0]
        l1.append(list0)

    # 列表只有两个元素的时候
    elif len(htmlList)>1:
        l2 = htmlList
        list00 = l2[0]
        del l2[0]
        l2.append(list00)

    else:
        pass
    return htmlList

def getTitle(htmllist):
    htmllist = str(htmllist)
    htmltitle = re.findall('<a href=".*?">(.*?)</a>',htmllist)
    return htmltitle


def getUrl(htmllist):
    htmllist = str(htmllist)
    htmlurl = re.findall('<a href="(.*?)">',htmllist)
    # 给url 加上前缀，是url 变成有效的url
    urllist = []
    for url in htmlurl:
        newurl = f"https://m.sinodan.cc{url}"
        urllist.append(newurl)
    return urllist


def makelist(menu,titlelist, urllist):
    if os.path.exists(f"{menu}.txt"):
        print(f'{menu}.txt文件夹已经存在')
    else:
        fp = open(f'{menu}.txt','w',encoding="utf-8") #创建txt文件
        print('正在下载小说：', menu)
        fp.close()
        datalist = []  # 定义一个存储所有数据的list
        for i in range(0,len(urllist)):

            html = getHtml(urllist[i])
            soup = getSoup(html)
            data = soup.find_all("p")  # 查找所有的span
            result = [a.get_text() for a in data]
            datalist.append(titlelist[i]) # 每个章节前面插入标题
            datalist.append('\n')       # 标题结束换行

            print(f'正在下载第{i+1}章...')
            for value in result:
                if len(value) > 400:
                    # value = unicode(value, "utf-8")
                    datalist.append(value)
                    datalist.append('\n')   # 章节结束换行
        datalist = ''.join(datalist)

        fp = open(f'{menu}.txt','w',encoding="utf-8")
        fp.write(str(datalist))
        fp.close()


def getIndexList(indexsoup):
    indexlist =[]
    indexurl = indexsoup.find_all("a", {"class":{"name"}})
    for i in indexurl:
        # https://m.sinodan.cc/list/11730.html
        i = i['href']
        url_i = f'https://m.sinodan.cc{i}'
        indexlist.append(url_i)
    return indexlist

def index(indexurl):
    for url in indexurl:
        html = getHtml(url)     # 这个url 是一本书的主页面 如：https://m.sinodan.cc/list/1405.html
        soup = getSoup(html)
        menu = getmenu(soup)
        htmllist = getList(soup) # 通过css 选择器等处理，得到htmlList列表（此时顺序不对）
        order_by(htmllist)  # 用排序方法来处理一下
        titlelist = getTitle(htmllist)
        urllist = getUrl(htmllist)
        makelist(menu,titlelist,urllist)   # 逐个下载列表里面的数据，需要传两个参数进去：menu titlelist urllist


def multiple(htmlListall):

    # 定义多个列表
    htmllist0 = []
    htmllist1 = []
    htmllist2 = []
    htmllist3 = []
    htmllist4 = []
    htmllist5 = []
    htmllist6 = []
    htmllist7 = []
    htmllist8 = []
    # 将列表中的任务分配给对应的进程 该段代码后续需要优化
    for i in range(len(htmlListall)):
        if i % 9 == 0:
            htmllist0.append(htmlListall[i])
        elif i % 9 == 1:
            htmllist1.append(htmlListall[i])
        elif i % 9 == 2:
            htmllist2.append(htmlListall[i])
        elif i % 9 == 3:
            htmllist3.append(htmlListall[i])
        elif i % 9 == 4:
            htmllist4.append(htmlListall[i])
        elif i % 9 == 5:
            htmllist5.append(htmlListall[i])
        elif i % 9 == 6:
            htmllist6.append(htmlListall[i])
        elif i % 9 == 7:
            htmllist7.append(htmlListall[i])
        else:
            htmllist8.append(htmlListall[i])

    # 创建进程
    process_dl0 = multiprocessing.Process(target=index, args=(htmllist0,))
    process_dl1 = multiprocessing.Process(target=index, args=(htmllist1,))
    process_dl2 = multiprocessing.Process(target=index, args=(htmllist2,))
    process_dl3 = multiprocessing.Process(target=index, args=(htmllist3,))
    process_dl4 = multiprocessing.Process(target=index, args=(htmllist4,))
    process_dl5 = multiprocessing.Process(target=index, args=(htmllist5,))
    process_dl6 = multiprocessing.Process(target=index, args=(htmllist6,))
    process_dl7 = multiprocessing.Process(target=index, args=(htmllist7,))
    process_dl8 = multiprocessing.Process(target=index, args=(htmllist8,))

    # print("完成")
    # 启动进程
    process_dl0.start()         #封印未开
    process_dl1.start()       #牛刀小试
    process_dl2.start()       #三倍快乐
    process_dl3.start()       #IP被封
    process_dl4.start()       #用不上啦
    process_dl5.start()  # 封印未开
    process_dl6.start()  # 牛刀小试
    process_dl7.start()  # 三倍快乐
    process_dl8.start()  # IP被封



def main():
    # 请输入你需要爬取的网站url 当前爬取的网站是 第一版主的镜像网站 https://m.sinodan.cc
    # url = 'https://m.sinodan.cc/list/2604.html'   #多条数据
    indexurl_sum =[]
    for aa in range(18,25):
        indexurl = f'https://m.sinodan.cc/book/8490_{aa}.html' # 网站数据的第一页，包含20多本书
        indexhtml = getHtml(indexurl)
        indexsoup = getSoup(indexhtml)
        indexurl = getIndexList(indexsoup) # 该url列表是主页的url列表
        for i in indexurl:
            indexurl_sum.append(i)
    indexurl = indexurl_sum     # 将多页的url合并在一个列表里面
    multiple(indexurl)


if __name__ == '__main__':
    main()
