#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf-8 -*-
import urllib2,sys
import bs4,re,socket,time
from bs4 import BeautifulSoup
"""
抓取网页信息（影片名、下载量、海报图片url等）
"""
class WebCrawl:
    def __init__(self,name,url,type):
        self.name=name
        self.url=url
        self.type=str(type)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.2; rv:7.0.1) Gecko/20100101 FireFox/7.0.1'}
        self.req=urllib2.Request(self.url,headers=self.headers)
        self.info=urllib2.urlopen(self.req).info()
        if(self.info.getparam('charset')):self.charset=self.info.getparam('charset')
        else:self.charset='utf8'
    def crawl_content(self,url):
        try:
            socket.setdefaulttimeout(10)
            req=urllib2.Request(url,headers=self.headers)
            content=urllib2.urlopen(req).read()
            return unicode(content,self.charset)
        except Exception as e:
            print url
    def parse_num(self,text):
        num_pattern = ur'\d+'
        m=re.search(num_pattern,text)
        return m.group()
    def crawl(self,url,crawl_info):
        content=self.crawl_content(url)
        while content == None:
            time.sleep(1)
            content=self.crawl_content(url)
        soup = BeautifulSoup(content)
        target = soup.findAll(crawl_info['block']['tag'],crawl_info['block']['attr'])
        raw_info = list()
        update_time = time.strftime('%Y-%m-%d',time.localtime())
        for item in target:
            title=item.find(crawl_info['title']['tag'],crawl_info['title']['attr']).text
            num=self.parse_num(item.find(crawl_info['num']['tag'],crawl_info['num']['attr']).text)
            img=item.find(crawl_info['img']['tag'],crawl_info['img']['attr']).attrs['src']
            raw_info.append({'raw_title':title,'num':num,'pic_url':img,'source_site':self.name,'type':self.type,'update_time':update_time})
        print '%s has been done, got %d records' % (url,len(raw_info))
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
    myegy = WebCrawl('myegy_ar',url,0)
    result = myegy.crawl(url,arabseed_desc)
    for line in result:
        print 'Raw_Title:%s' % (line['raw_title'].encode('utf8'))
if __name__ == '__main__':
    main()
