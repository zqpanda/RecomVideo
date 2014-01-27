#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf-8 -*-
import MySQLdb as mdb
import os,re,time,sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../bin/')
import crawl as ca

def crawl(cmd,type,url,page=[],suffix=''):
    title = list()
    num = list()
    img = list()
    movie_info = list()
    cmd_prefix = {
        'phantomjs':'phantomjs /home/hao123/users/zhouqiang/script/video_recom_src/bin/',
        'python':'/home/hao123/tools/python/bin/python2.7 /home/hao123/users/zhouqiang/script/video_recom_src/bin/'
    }
    cmd = cmd_prefix[type]+cmd+' '
    for page_num in page:
        res = os.popen(cmd+url+page_num+suffix).readlines()
        for line in res:
            line = line.strip()
            if line.startswith('Title:'):title.append(line[6:])
            if line.startswith('Num:'):num.append(line[4:])
            if line.startswith('Img'):img.append(line[4:])
        print url,page_num,' has finished!'
    for i in range(len(title)):
        movie_info.append({'title':title[i],'num':num[i],'img_url':img[i]})
    return movie_info

def insert_to_db(movie_info,type,source_site):
    conn = mdb.connect(host="10.48.47.34",user="xiaoling",passwd="xiaoling",db="video_recom_ar",port=6001,charset="utf8")
    cursor = conn.cursor()
    update_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sql = "insert into movie_raw_data(raw_title,num,type,source_site,update_time,pic_url) values (%s,%s,%s,%s,%s,%s)"
    for item in movie_info:
        param = (item['title'],item['num'],type,source_site,update_time,item['img_url'])
        n = cursor.execute(sql,param)
        if n:conn.commit()
    cursor.close()
    conn.close()

def raw_title_trim():
    conn = mdb.connect(host="10.48.47.34",user="xiaoling",passwd="xiaoling",db="video_recom_ar",port=6001,charset="utf8")
    cursor = conn.cursor()
    cursor.execute('set names utf8')
    sql = 'select raw_title from movie_raw_data where title is null'
    n = cursor.execute(sql)
    for row in cursor.fetchall():
        print row[0].encode('utf8')

def main():
    arabseed_info={
        'cmd':'arabseed.js',
        'type':'phantomjs',
        'd_url':'http://www.arabseed.com/ar/category/view/41/',
        'f_url':'http://www.arabseed.com/ar/category/view/42/',
        'page_list':['','36/','72/','108/','144/'],
    }
   # arabseed_data_d = crawl(arabseed_info['cmd'],arabseed_info['type'],arabseed_info['d_url'],arabseed_info['page_list'])
   # arabseed_data_f = crawl(arabseed_info['cmd'],arabseed_info['type'],arabseed_info['d_url'],arabseed_info['page_list'])
   # insert_to_db(arabseed_data_d,1,'http://www.arabseed.com/')
   # insert_to_db(arabseed_data_f,1,'http://www.arabseed.com/')
    myegy_info={
        'cmd':'myegy.py',
        'type':'python',
        'ar_url':'http://myegy.com/arabic-movies/',
		'en_url':'http://myegy.com/english-movies/',
        'in_url':'http://myegy.com/in-movies/',
        'page_list':['','p2/','p3/','p4/','p5/'],
    }
    cima4u_info={
        'cmd':'cima4u.js',
        'type':'phantomjs',
        'url':'http://cima4u.com/',
        'page_list':['','p2.html','p3.html','p4.html','p5.html'],
    }
    mazika2day_info={
        'cmd':'mazika2day.js',
        'type':'phantomjs',
        'd_url':'http://mazika2day.com/cat,1,',
        'f_url':'http://mazika2day.com/cat,3,',
        'd_suffix':'%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9.html',
        'f_suffix':'%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9.html',
        'page_list':['','2,','3,','4,','5,'],
    }
    raw_title_trim()
#    cima4u_data = crawl(cima4u_info['cmd'],cima4u_info['type'],cima4u_info['url'],cima4u_info['page_list'])
#    mazika2day_data_d = crawl(mazika2day_info['cmd'],mazika2day_info['type'],mazika2day_info['d_url'],mazika2day_info['page_list'],mazika2day_info['d_suffix'])
#    mazika2day_data_f = crawl(mazika2day_info['cmd'],mazika2day_info['type'],mazika2day_info['f_url'],mazika2day_info['page_list'],mazika2day_info['f_suffix'])
	
#    myegy_data_ar = crawl(myegy_info['cmd'],myegy_info['type'],myegy_info['ar_url'],myegy_info['page_list'])
#    myegy_data_en = crawl(myegy_info['cmd'],myegy_info['type'],myegy_info['en_url'],myegy_info['page_list'])
#    myegy_data_in = crawl(myegy_info['cmd'],myegy_info['type'],myegy_info['in_url'],myegy_info['page_list'])
##    print len(myegy_data_ar),len(myegy_data_en),len(myegy_data_in)
#    insert_to_db(myegy_data_ar,1,'http://myegy.com/')
#    insert_to_db(myegy_data_en,1,'http://myegy.com/')
#    insert_to_db(myegy_data_in,1,'http://myegy.com/')
    print 'Done'
if __name__ == '__main__':
    main()

