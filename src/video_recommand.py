#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf8 -*-
import os, sys
import ConfigParser
import time
#import re
import string
sys.path.append('../bin/')
from restore import MySQLDB

#参数读取
def para_read(para_path):
    cf = ConfigParser.ConfigParser()
    cf.read(para_path)
    return cf
#获取配置信息
def get_global_conf():
    config = ConfigParser.ConfigParser()
    config.read(global_conf_dir+"global_video_recommand.conf")
    return config
#数据来源
def deal_data_source(config, type):
    print "deal_%s_source" % (type)
    source_num=config.get(type+"_source", "source_num")
    print source_num
    for i in xrange(int(source_num)):
        print config.get(type+"_source", "get_info"+str(i))
#获取数据库配置信息
def get_db_conf():
    db_cf = para_read('../conf/db.conf')
    db_conf = {
        'host' : db_cf.get('db','db_host'),
        'user' : db_cf.get('db','db_user'),
        'passwd' : db_cf.get('db','db_pass'),
        'port' : db_cf.getint('db','db_port')
    }
    return db_conf
#从数据库中获取raw data
def get_movie_data_from_db(db_conf):
    mydb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    mydb.selectDb('video_recom_ar')
    sql = 'select * from movie_raw_data where update_time = \'2014-2-9\''
    raw_data = mydb.queryAll(sql)
    mydb.close()
    return raw_data
#获取站点信息（如站点类型及权值）
def get_url_info(db_conf):
    mydb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    mydb.selectDb('video_recom_ar')
    sql = 'select * from url_info'
    url_info = mydb.queryAll(sql)
    mydb.close()
    return url_info
#影片信息汇总，以trim-title作为key值
def organize_data(movie_data):
    organized_data = dict()
    for record in movie_data:
        if record['title'] not in organized_data.keys():
            organized_data[record['title']]

#主程序
def main():
    global_config = get_global_conf()
    deal_data_source(global_config, "online")
    db_conf = get_db_conf()
    movie_data = get_movie_data_from_db(db_conf)
    url_info = get_url_info(db_conf)
    print url_info
    '''
    organize_list = []
    print raw_data
    trim_list = get_trim_list()
    raw_date_after_trim = trim_movie_name(raw_data, trim_list)
    print raw_date_after_trim
    trim_key_list = organize_trim_key(raw_date_after_trim, organize_list)
    print trim_key_list
    first_adjust_result = first_adjust_weight(trim_key_list, site_weight)
    print first_adjust_result
    sort_weight_list = insert_sort(first_adjust_result)
    print sort_weight_list
    '''
if __name__ == '__main__':
    main()



