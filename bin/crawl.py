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

def crawl(url,**page_description):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.2; rv:7.0.1) Gecko/20100101 FireFox/7.0.1'}
    req=urllib2.Request(url,headers=headers)
    f = urllib2.urlopen(req).info()
    charset = f.getparam('charset')
    content=urllib2.urlopen(req).read()
    soup = BeautifulSoup(content)
    target = soup.findAll(page_description['block'],id=page_dscription['block_id'])
    raw_info = list()
    for item in target:
        title = item.find(page_description['title']).text
        num = parse_num(item.find(page_description['num']).text)
        img = item.find(page_description['img']).attrs['src']
        raw_info.append({'Title':title,'Num':num,'Img':img})
    return raw_info
