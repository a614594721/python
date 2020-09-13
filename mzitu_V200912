# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import random
import requests
import os
import multiprocessing
from bs4 import BeautifulSoup
import time
import re
import urllib.request

index_top = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="gbk">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>home_page</title>

<link rel="stylesheet" href="css/waterfall.css">
<!-- 不兼容IE10以下浏览器 -->

</head>
<body>'''
index_end = '''</body>
</html>'''
moban_top = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="gbk">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>CSS3响应式瀑布流图片展示DEMO演示</title>

<link rel="stylesheet" href="../css/waterfall.css">
<!-- 不兼容IE10以下浏览器 -->

</head>
<body>

<!-- <h1>纯CSS3实现倾角瀑布流，带滤镜特效</h1> -->

<div style="text-align:center;clear:both;margin-bottom:50px;">
<script src="/gg_bd_ad_720x90.js" type="text/javascript"></script>
<script src="/follow.js" type="text/javascript"></script>
</div>

<div id="waterfall">
'''
moban_end = '''</div>

</body>
</html>
'''
waterfull_css ='''/* http://meyerweb.com/eric/tools/css/reset/ 
   v2.0 | 20110126
   License: none (public domain)
*/
html,
body,
div,
span,
applet,
object,
iframe,
h1,
h2,
h3,
h4,
h5,
h6,
p,
blockquote,
pre,
a,
abbr,
acronym,
address,
big,
cite,
code,
del,
dfn,
em,
img,
ins,
kbd,
q,
s,
samp,
small,
strike,
strong,
sub,
sup,
tt,
var,
b,
u,
i,
center,
dl,
dt,
dd,
ol,
ul,
li,
fieldset,
form,
label,
legend,
table,
caption,
tbody,
tfoot,
thead,
tr,
th,
td,
article,
aside,
canvas,
details,
embed,
figure,
figcaption,
footer,
header,
hgroup,
menu,
nav,
output,
ruby,
section,
summary,
time,
mark,
audio,
video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article,
aside,
details,
figcaption,
figure,
footer,
header,
hgroup,
menu,
nav,
section {
  display: block;
}
body {
  line-height: 1;
}
ol,
ul {
  list-style: none;
}
blockquote,
q {
  quotes: none;
}
blockquote:before,
blockquote:after,
q:before,
q:after {
  content: '';
  content: none;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
}
* {
  box-sizing: border-box;
  font-family: "微软雅黑";
}
h1 {
  text-align: center;
  padding: 50px  0;
  font-size: 32px;
  font-weight: bold;
  color: #333;
}
#waterfall {
  column-count: 3; 
  width: 80%;
  margin: 0 auto;
  column-gap: 15px;
}
#waterfall > span {
  margin-bottom: 20px;
  display: block;
  overflow: hidden;
}
#waterfall > span img {
  display: block;
  width: 100%;
  transform: rotate(4deg);
  opacity: 0.9;
  filter: saturate(150%);
}
#waterfall > span:hover img {
  transform: rotate(0deg);
  transform: scale(1.15);
  transition: all 200ms linear;
  opacity: 1;
  filter: saturate(100%);
}
'''
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

    soup= BeautifulSoup(html.text, "html.parser")
    return soup

def getTitle(soup):
    title = soup.title.contents[0]
    # '_'所在的索引位置
    number = title.index(' ')
    title = title[:number]
    new_title = re.sub(r"|[\\/:*?\"<>| ]+", "", title)
    return str(new_title)


def getAllPage(soup):
    allPage = soup.select('.pagenavi > a > span')[-2].string
    return allPage

def getdefurl(soup):
    defurl = soup.select(".main-image > p > a > img ")[0].attrs['src'][0:-6]
    return defurl

# 创建文件夹及文件
def makedir(title):
    try:
        os.mkdir(f'Picture/{title}')
        return 0
    except:
        print(f"{title} 该文件夹无法被创建，可能原因是该文件夹已经存在！！！\n")
        return 1


def makehtml(title, count):
    # os.mkdir(title)
    # print("xxxxxx")
    fp = open(f"HTML/{title}.html", 'w')
    fp.write(moban_top)

    for i in range(1,count):
        fp.write(f'<span><img src="../Picture/{title}/{i}.jpg" ></span>\n')
        # fp.next()
    fp.write(moban_end)
    fp.close()

def makeindexhtml(title):
    lines = []
    f = open("index.html", 'r')  # your path!
    for line in f:
        lines.append(line)
    f.close()
    lines.insert(13, f"<h2><a href=\"HTML/{title}.html\">{title}</a></h2>\n")  # 第13行后面插入数据
    s = ''.join(lines)
    f = open("index.html", 'w+')  # 重新写入文件
    f.write(s)
    f.close()
    del lines[:]  # 清空列表

def downloadPic(title, allPage, defurl):
    makehtml(title,int(allPage)+1)
    makeindexhtml(title)
    for number in range(1, int(allPage) + 1):
        picUrl = f"{defurl}{str(number).rjust(2, '0')}.jpg"
        # print(picUrl)   # https://imgpc.iimzt.com/2017/12/18a01.jpg
        pic = getHtml(picUrl)
        with open(f"Picture/{title}/{number}.jpg", "wb+") as f:
            f.write(pic.content)
            print(f"第{number}张图片，正在下载中...")
            time.sleep(random.uniform(0, 1))
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
        # print(htmlMark)
        try:
            html = getHtml(f"{htmlMark}")
            soup = getSoup(html)
            title = getTitle(soup)      # 需要爬取网页的标题
            allPage = getAllPage(soup)  #该标题下面的图片总个数
            defurl = getdefurl(soup)    #默认的url
            new_title = title
            #new_title = title + htmlMark
            # print(new_title)  #输出文件夹的名字
            makedir_value = makedir(new_title)

        except:
            print("%s网页出现了错误" % htmlMark)
            continue
        if makedir_value == 0:
            downloadPic(new_title, allPage, defurl)
        else:
            # print("break")
            continue



def multiple(multipe_count):

    # 定义多个列表
    htmllist0 = []
    htmllist1 = []
    htmllist2 = []
    htmllist3 = []
    htmllist4 = []
    # 将列表中的任务分配给对应的进程 该段代码后续需要优化
    for i in range(len(htmlListall)):
        if i % 2 == 0:
            htmllist0.append(htmlListall[i])
        elif i % 5 == 1:
            htmllist1.append(htmlListall[i])
        elif i % 5 == 2:
            htmllist2.append(htmlListall[i])
        elif i % 5 == 3:
            htmllist3.append(htmlListall[i])
        else:
            htmllist1.append(htmlListall[i])

    #将列表转换成元组 注释了这一段代码，程序能正常运行，似乎这段代码没有受到影响
    # htmllist0 = tuple(htmllist0)
    # htmllist1 = tuple(htmllist1)
    # htmllist2 = tuple(htmllist2)
    # htmllist3 = tuple(htmllist3)
    # htmllist4 = tuple(htmllist4)


    # 创建进程
    process_dl0 = multiprocessing.Process(target=index, args=(0,htmllist0))
    process_dl1 = multiprocessing.Process(target=index, args=(1,htmllist1))
    process_dl2 = multiprocessing.Process(target=index, args=(2,htmllist2))
    process_dl3 = multiprocessing.Process(target=index, args=(3,htmllist3))
    process_dl4 = multiprocessing.Process(target=index, args=(4,htmllist4))
    # print("完成")
    # 启动进程
    process_dl0.start()         #封印未开
    process_dl1.start()       #牛刀小试
    # process_dl2.start()       #三倍快乐
    # process_dl3.start()       #IP被封
    # process_dl4.start()       #用不上啦


if __name__ == '__main__':
    # 在程序开始之前，先准备需要的文件夹和文件
    # 创建文件夹
    try:
        os.mkdir('HTML')
    except:
        pass
        # print('HTML文件夹已经存在')
    try:
        os.mkdir('Picture')
    except:
        pass
        # print('Picture文件夹已经存在')
    try:
        os.mkdir('css')
    except:
        pass
        # print('css文件夹已经存在')
    # 创建index.html文件
    # 先判断文件是否存在
    if os.path.exists("index.html"):
        pass
        # print('index.html文件夹已经存在')
    else:
        f = open("index.html", 'w')  # your path!
        f.write(index_top)
        f.write('\n')
        f.write(index_end)
        f.close()

    if os.path.exists("css\waterfall.css"):
        pass
        # print('css\waterfall.css文件夹已经存在')
    else:
        f = open("css\waterfall.css", 'w')  # your path!
        f.write(waterfull_css)
        f.close()
    # 请输入你需要爬取的网站模块
    url = f'https://www.mzitu.com/page/52/'

    html = getHtml(url)
    soup = getSoup(html)
    htmlList = soup.select(".postlist > ul > li > a")

    htmlListall = []
    for url in htmlList:
        a = url['href']
        htmlListall.append(a)
    # print(htmlListall)  # 当前页面所有图片连接的合集
    # 启用
    #定义进程的个数
    multipe_count = 2
    multiple(multipe_count)
