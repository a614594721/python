import requests
import os
from bs4 import BeautifulSoup


def getHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Referer": "https://www.mm131.net"
        }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    return html


def getSoup(html):
    return BeautifulSoup(html.text, "html.parser")


def getTitle(soup):
    title = soup.title.contents[0]
    # '_'所在的索引位置
    number = title.index('_')
    title = title[:number]
    return str(title)


def getAllPage(soup):
    allPage = soup.select('body > div.content > div.content-page > span:nth-child(1)')[0].string[1:-1]
    return allPage


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

def downloadPic(title, allPage, htmlMark):
    for number in range(1, int(allPage) + 1):
        picUrl = f"https://img1.mmmw.net/pic/{htmlMark}/{number}.jpg"
        pic = getHtml(picUrl)
        try:
            with open(f"{title}/{number}.jpg", "wb+") as f:
                f.write(pic.content)
                print(f"第{number}张图片，正在下载中...")
        except:
            with open(f"默认文件夹/{htmlMark}_{number}.jpg", "wb+") as f:
                f.write(pic.content)
                print(f"第{number}张图片，正在下载中...")
def main():
    # 请输入你需要爬取的页码
    for mark in range(5470, 0, -1):
        htmlMark = str(mark)
        try:
            html = getHtml(f"https://www.mm131.net/xinggan/{htmlMark}.html")
            soup = getSoup(html)
            title = getTitle(soup)
            allPage = getAllPage(soup)
            new_title = title + '_page=' + htmlMark
            #new_title = title + htmlMark
            print(new_title)
            makedir(new_title)
        except:
            print("%s网页出现了错误" % htmlMark)
            continue
        downloadPic(new_title, allPage, htmlMark)


if __name__ == '__main__':
    main()
