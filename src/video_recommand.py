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
    config.read('../conf/global_video_recommand.conf')
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
    sql = 'select * from movie_raw_data where update_time = \'2014-2-14\''
    raw_data = mydb.queryAll(sql)
    trim_conf_file = '../conf/trim_list.conf'
    input_file_handler = open(trim_conf_file)
    trim_list = []
    for line in input_file_handler.readlines():
        line = line.strip()
        trim_list.append(line)
    input_file_handler.close()
    update_count = 0
    for i in xrange(len(raw_data)):
        temp_name = raw_data[i]["raw_title"]
        old_title = raw_data[i]["title"]
        for j in xrange(len(trim_list)):
            temp_name = temp_name.replace(trim_list[j],'')
        if old_title != temp_name.strip():
            update_count += 1
#            print 'Stop';sys.exit()
            new_title = mydb.escape_string(temp_name.strip())
            raw_data[i]["title"] = new_title
            id = raw_data[i]["id"]
            update_sql = 'update movie_raw_data set title = \''+new_title+'\' where id = \''+id+'\''
            mydb.query(update_sql)
            mydb.commit()
    print '%d records have been updated' % (update_count)
    mydb.close()
    return raw_data
#获取站点信息（如站点类型及权值）
def get_weight_dict(db_conf):
    mydb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    mydb.selectDb('video_recom_ar')
    sql = 'select url_name,url_type,url_weight from url_info'
    url_info = mydb.queryAll(sql)
    weight_dict = dict()
    for item in url_info:
        weight_dict[item['url_name']]={
            'type':item['url_type'],
            'weight':int(item['url_weight'])
        }
    mydb.close()
    return weight_dict
#影片信息汇总，以trim-title作为key值
def organize_data(movie_data):
    organized_data = dict()
    for record in movie_data:
        pos = record['source_site'].find('_')
        source_site=record['source_site']
        if pos != -1: source_site=record['source_site'][:pos]
        title=record['title']
        num=int(record['num'])
        if not organized_data.has_key(title):
            organized_data[title]={
                source_site:num
            }
        elif organized_data[title].has_key(source_site):
            organized_data[title][source_site]+=num
        else:
            organized_data[title][source_site]=num
    return organized_data
#计算影片得分
def first_adjust_weight(organized_data,weight_dict):
    movie_score=dict()
    for k,v in organized_data.iteritems():
        sum_of_weight = {
            '0':0,
            '1':0,
            '2':0
        }
        for site,num in v.iteritems():
            if weight_dict[site]['type'] == '0':sum_of_weight['0'] += weight_dict[site]['weight']*num
            else:sum_of_weight['1'] += weight_dict[site]['weight']*num
        movie_score[k] = sum_of_weight
    return movie_score

#将影片得分整理入库
def sort_insert_db(db_conf,movie_score):
    mydb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    mydb.selectDb('video_recom_ar')
    update_time = time.strftime('%Y-%m-%d',time.localtime())
    clean_old_score = 'delete from movie_score where update_time = \''+update_time+'\''
    mydb.query(clean_old_score)
    mydb.commit()
    for title,score_dict in movie_score.iteritems():
        total_score = score_dict['0'] + score_dict['1'] + score_dict['2']
        mydb.insert('movie_score',{'title':title,'online_score':str(score_dict['0']),'download_score':str(score_dict['1']),'rank_score':str(score_dict['2']),'score':str(total_score),'update_time':update_time})
    mydb.commit()
    mydb.close()
    return


#主程序
def main():
#    global_config = get_global_conf()
#    deal_data_source(global_config, "online")
    db_conf = get_db_conf()
    movie_data = get_movie_data_from_db(db_conf)
    weight_dict = get_weight_dict(db_conf)
    organized_data = organize_data(movie_data)
    movie_score=first_adjust_weight(organized_data,weight_dict)
#    print len(movie_score)
    sort_insert_db(db_conf,movie_score)
    print 'Finished'

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



