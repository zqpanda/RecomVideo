#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf-8 -*-
import urllib2,sys
import bs4,re
from bs4 import BeautifulSoup
"""
抓取网页信息（影片名、下载量、海报图片url等）
"""
def parse_num(text):
    num_pattern = ur'\d+'
    m = re.search(num_pattern,text)
    return m.group()

def crawl(url,page_desc):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.2; rv:7.0.1) Gecko/20100101 FireFox/7.0.1'}
    req=urllib2.Request(url,headers=headers)
    f = urllib2.urlopen(req).info()
    charset = f.getparam('charset')
    content=urllib2.urlopen(req).read()
    soup = BeautifulSoup(content)
    target = soup.findAll(page_desc['block']['tag'],page_desc['block']['attr'])
    raw_info = list()
    for item in target:
        title = item.find(page_desc['title']['tag'],page_desc['title']['attr']).text
        num = parse_num(item.find(page_desc['num']['tag'],page_desc['num']['attr']).text)
        img = item.find(page_desc['img']['tag'],page_desc['img']['attr']).attrs['src']
        raw_info.append({'Title':title,'Num':num,'Img':img})
    return raw_info
def main():
    myegy_desc = {
        'block':{'tag':'div','attr':{'id':'topic'}},
        'title':{'tag':'h1','attr':{}},
        'num':{'tag':'div','attr':{}},
        'img':{'tag':'img','attr':{}}
    }
    cima4u_desc = {
        'block':{'tag':'table','attr':{'class':'art_content'}},
        'title':{'tag':'a','attr':{'class':'title_a'}},
        'num':{'tag':'a','attr':{'class':'dwn_a'}},
        'img':{'tag':'img','attr':{'class':'art_image_1'}}
    }
    arabseed_desc = {
        'block':{'tag':'div','attr':{'class':'normal'}},
        'title':{'tag':'div','attr':{'class':'titag'}},
        'num':{'tag':'div','attr':{'class':'downdiv'}},
        'img':{'tag':'img','attr':{'class':'photo'}}
    }
    mazika2day_desc = {
        'block':{'tag':'div','attr':{'class':'box'}},
        'title':{'tag':'h3','attr':{}},
        'num':{'tag':'b','attr':{}},
        'img':{'tag':'img','attr':{}}
    }
    url = sys.argv[1]
    result = crawl(url,mazika2day_desc)
    for item in result:
        print item

if __name__ == '__main__':
    main()
