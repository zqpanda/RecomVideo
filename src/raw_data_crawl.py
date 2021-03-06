#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf-8 -*-
import os,re,time,sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../bin/')
from crawl import WebCrawl 
from restore import MySQLDB
import ConfigParser

#配置文件读取
def para_read(para_path):
    cf = ConfigParser.ConfigParser()
    cf.read(para_path)
    return cf
#电影名过滤
def raw_title_trim(raw_data):
    '''
    conn = mdb.connect(host="10.48.47.34",user="xiaoling",passwd="xiaoling",db="video_recom_ar",port=6001,charset="utf8")
    cursor = conn.cursor()
    cursor.execute('set names utf8')
    sql = 'select raw_title from movie_raw_data where title is null'
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print row[0].encode('utf8')
    '''
    trim_conf_file = '../conf/trim_list.conf'
    input_file_handler = open(trim_conf_file)
    trim_list= []
    for line in input_file_handler.readlines():
        line=line.strip()
        trim_list.append(line.decode('utf8'))
    input_file_handler.close()

    for i in xrange(len(raw_data)):
        temp_name = raw_data[i]["raw_title"]
        for j in xrange(len(trim_list)):
            temp_name = temp_name.replace(trim_list[j],'')
        raw_data[i]["title"] = temp_name.strip()
    return raw_data

#主程序
def main():
    #被抓取网站配置信息包括url及抓取页面编号
    urls_conf = para_read('../conf/urls.conf')
    arabseed_info={
        'd_url':urls_conf.get('arabseed','d_url'),
        'f_url':urls_conf.get('arabseed','f_url'),
        'page_list':['','36/','72/','108/','144/'],
    }
    myegy_info={
        'ar_url':urls_conf.get('myegy','ar_url'),
		'en_url':urls_conf.get('myegy','en_url'),
        'in_url':urls_conf.get('myegy','in_url'),
        'page_list':['','p2/','p3/','p4/','p5/'],
    }
    cima4u_info={
        'url':urls_conf.get('cima4u','url'),
        'ar_url':urls_conf.get('cima4u','ar_url'),
        'en_url':urls_conf.get('cima4u','en_url'),
        'in_url':urls_conf.get('cima4u','in_url'),
        'page_list':['.html','-p2.html','-p3.html','-p4.html','-p5.html'],
    }
    mazika2day_info={
        'd_url':urls_conf.get('mazika2day','d_url'),
        'f_url':urls_conf.get('mazika2day','f_url'),
        'd_suffix':urls_conf.get('mazika2day','d_suffix'),
        'f_suffix':urls_conf.get('mazika2day','f_suffix'),
        'page_list':['.html',',2.html',',3.html',',4.html',',5.html'],
    }
    myegy_desc = {
        'block':{'tag':'div','attr':{'id':'topic'}},
        'title':{'tag':'h1','attr':{}},
        'num':{'tag':'div','attr':{}},
        'img':{'tag':'img','attr':{}},
    }
    cima4u_desc = {
        'block':{'tag':'table','attr':{'class':'art_content'}},
        'title':{'tag':'a','attr':{'class':'title_a'}},
        'num':{'tag':'a','attr':{'class':'dwn_a'}},
        'img':{'tag':'img','attr':{'class':'art_image_1'}},
    }
    arabseed_desc = {
        'block':{'tag':'div','attr':{'class':'normal'}},
        'title':{'tag':'div','attr':{'class':'titag'}},
        'num':{'tag':'div','attr':{'class':'downdiv'}},
        'img':{'tag':'img','attr':{'class':'photo'}},
    }
    mazika2day_desc = {
        'block':{'tag':'div','attr':{'class':'box'}},
        'title':{'tag':'h3','attr':{}},
        'num':{'tag':'b','attr':{}},
        'img':{'tag':'img','attr':{}},
    }
    #数据库配置文件读取
    db_cf = para_read('../conf/db.conf')
    db_conf = {
        'host' : db_cf.get('db','db_host'),
        'user' : db_cf.get('db','db_user'),
        'passwd' : db_cf.get('db','db_pass'),
        'port' : db_cf.getint('db','db_port')
    }
    #内容抓取cima4u
    cima4u_ar = WebCrawl('cima4u_ar',cima4u_info['url'],0)
    cima4u_en = WebCrawl('cima4u_en',cima4u_info['url'],0)
    cima4u_in = WebCrawl('cima4u_in',cima4u_info['url'],0)
    cima4u_data = list()
    for page in cima4u_info['page_list']:
        cima4u_data.extend(cima4u_ar.crawl(cima4u_info['ar_url']+page,cima4u_desc))
        cima4u_data.extend(cima4u_en.crawl(cima4u_info['en_url']+page,cima4u_desc))
        cima4u_data.extend(cima4u_in.crawl(cima4u_info['in_url']+page,cima4u_desc))
    print 'Cima4u finished! Got %d records' %(len(cima4u_data))
    #myegy
    myegy_ar = WebCrawl('myegy_ar',myegy_info['ar_url'],1)
    myegy_en = WebCrawl('myegy_en',myegy_info['en_url'],1)
    myegy_in = WebCrawl('myegy_in',myegy_info['in_url'],1)
    myegy_data = list()
    for page in myegy_info['page_list']:
        myegy_data.extend(myegy_ar.crawl(myegy_info['ar_url']+page,myegy_desc))
        myegy_data.extend(myegy_en.crawl(myegy_info['en_url']+page,myegy_desc))
        myegy_data.extend(myegy_in.crawl(myegy_info['in_url']+page,myegy_desc))
    print 'Myegy finished! Got %d records' %(len(myegy_data))
    #arabseed
    arabseed_d = WebCrawl('arabseed_d',arabseed_info['d_url'],1)
    arabseed_f = WebCrawl('arabseed_f',arabseed_info['f_url'],1)
    arabseed_data = list()
    for page in arabseed_info['page_list']:
        arabseed_data.extend(arabseed_d.crawl(arabseed_info['d_url']+page,arabseed_desc))
        arabseed_data.extend(arabseed_f.crawl(arabseed_info['f_url']+page,arabseed_desc))
    print 'Arabseed finished! Got %d records' %(len(arabseed_data))
    #mazika2day
    mazika2day_d = WebCrawl('mazika2day_d',mazika2day_info['d_url']+mazika2day_info['d_suffix']+'.html',1)
    mazika2day_f = WebCrawl('mazika2day_f',mazika2day_info['f_url']+mazika2day_info['f_suffix']+'.html',1)
    mazika2day_data = list()
    for page in mazika2day_info['page_list']:
        mazika2day_data.extend(mazika2day_d.crawl(mazika2day_info['d_url']+mazika2day_info['d_suffix']+page,mazika2day_desc))
        mazika2day_data.extend(mazika2day_f.crawl(mazika2day_info['f_url']+mazika2day_info['f_suffix']+page,mazika2day_desc))
    print 'Mazika2day finished! Got %d records' %(len(mazika2day_data))
    
    #合并原始影片信息影片名称trim
    print 'Hi, We came here'
    all_raw_data = cima4u_data + myegy_data + arabseed_data + mazika2day_data
    trim_data = raw_title_trim(all_raw_data)
    print len(trim_data)
    #影片信息入库
    mydb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    mydb.selectDb('video_recom_ar')
    for record in trim_data:
        flag = mydb.insert('movie_raw_data',record)
        if flag == 0:print "Something is wrong %s" %(record)
    if flag != 0: mydb.commit()
    mydb.close()
#    for line in result:
#        print 'Raw Title: %s' % (line['raw_title'])
#    print 'Done'
#    trimed_data = raw_title_trim(raw_data)
#    for line in trimed_data:
#        print 'Raw_title: %s #### Trimed_title: %s' %(line['raw_title'].encode('utf8'),line['Trim_name'].encode('utf8'))


if __name__ == '__main__':
    main()

