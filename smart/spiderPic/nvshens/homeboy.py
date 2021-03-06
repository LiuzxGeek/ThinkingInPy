#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
from random import random
from time import sleep

from pkgUtils import getLevelPath
from urlUtils import getUserAgent, getHtml, getHtmlData

"""
第一步: 从 http://www.zngirls.com/rank/sum/ 开始抓取MM点击头像的链接(注意是分页的)
#第二部  http://www.zngirls.com/girl/21751/ 抓取每一个写真集合的链接(注意是分页的)
#第三部 http://www.zngirls.com/g/19671/1.html 在写真图片的具体页面抓取图片(注意是分页的)
"""

header = {
    "User-Agent": getUserAgent(6)
    , "Connection": "keep-alive"
}

"""
从起始页面 http://www.zngirls.com/rank/sum/ 开始获取排名的页数和每一页的url

"""


def mmRankSum():
    htmlPath = getHtml("https://www.zngirls.com/rank/sum/", header, 10)

    # 首先获取页码数,然后用循环的方式挨个解析每一个页面
    # 取得所有div目录下class标签值为pagesYY的节点，再取得此节点下的div标签下a标签为href的属性值
    pages = htmlPath.xpath('//div[@class="pagesYY"]/div/a/@href')

    length = len(pages)
    print(length)
    albums = []
    for i in range(length):
        subTitle = pages[i]
        pageItem = "http://www.zngirls.com/rank/sum/" + subTitle
        if pageItem in albums:
            continue
        else:
            albums.append(pageItem)
            print("pageItem:" + pageItem)
            mmRankitem(pageItem)

        """
        参数 url : 分页中每一页的具体url地址
        通过穿过来的参数，使用  lxml和xpath 解析 html，获取每一个MM写真专辑页面的url
        
        """


def mmRankitem(url):
    htmlPath = getHtml(url, header, 10)
    pages = htmlPath.xpath('//div[@class="rankli_imgdiv"]/a/@href')
    for i in range(len(pages)):
        # print  ("http://www.zngirls.com" + pages[i] + "album/")
        getAlbums("http://www.zngirls.com/" + pages[i] + "/album/")


"""
参数 url : 每一个MM专辑的页面地址
通过穿过来的参数，获取每一个MM写真专辑图片集合的地址

"""


def getAlbums(girlUrl):
    htmlPath = getHtml(girlUrl, header, 15)
    pages = htmlPath.xpath('//div[@class="igalleryli_div"]/a/@href')
    for i in range(len(pages)):
        albumPath = "http://www.zngirls.com" + pages[i]
        # print(albumPath)
        getPagePictures(albumPath)
        sleep(random.randint(1, 3))


"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址

"""


def getPagePictures(albumsUrl):
    htmlPath = getHtml(albumsUrl, header, 10)
    pages = htmlPath.xpath('//div[@id="pages"]/a/@href')
    albumName = htmlPath.xpath('//div[@class="albumTitle"]/h1/text()')[0]  # ("//body//h1[1]/text()")
    albums = []
    for i in range(len(pages)):
        screenPath = "http://www.zngirls.com" + pages[i]  # g/21450
        try:
            albums.index(screenPath)
            continue
        except ValueError:
            albums.append(screenPath)
        finally:
            # if i==0:
            # print(screenPath)
            savePictures(screenPath, albumName)


"""
参数 url : 每一个MM写真专辑图片集合的地址(进过分页检测)
通过穿过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。

"""


def savePictures(itemPagesurl, albumName):
    global pages
    header = {
        "User-Agent": getUserAgent(1),
        "Connection": "keep-alive",
        "Referer": "image / webp, image / *, * / *;q = 0.8",
        "Accept": "image/webp,image/*,*/*;q=0.8"
    }
    try:
        htmlPath = getHtml(itemPagesurl, header, 10)
        print(itemPagesurl)  # http://www.zngirls.com/g/27439/6.html
        pages = htmlPath.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')
        names = htmlPath.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt')
    except Exception as error:
        print("savePictures album parse Exception:")
    for i in range(len(pages)):
        print(pages[i])  # https://t1.onvshen.com:85/gallery/22784/27439/s/015.jpg
        try:
            headers = {
                "User-Agent": getUserAgent(1),
                "Connection": "keep-alive",
                "Referer": pages[i]
            }
            respHtml = getHtmlData(pages[i], headers, 10)
            cPath = getLevelPath(-2, '\\download\\meinv\\' + albumName + "\\")
            imgPath = '%s.jpg' % (cPath + names[i])
            if os.path.isfile(imgPath):
                pass
            else:
                binFile = open(imgPath, "wb")
                binFile.write(respHtml);
                binFile.close();
        except Exception as error:
            print("savePictures pic fetch Exception:")


mmRankSum()
print('finish')
# system('shutdown -s')
