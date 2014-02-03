import os, sys
import ConfigParser
#import MySQLdb
import time
#import re
import string
#global_conf = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+"/../conf/global_video_recommand.conf"
global_conf_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+"/../conf/"
data_addr = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+"/../data/"
tmp_addr = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+"/../tmp/"

def get_global_conf():
    config = ConfigParser.ConfigParser()
    config.read(global_conf_dir+"global_video_recommand.conf")
    return config

def get_trim_list():
    trim_conf_file = global_conf_dir+"trim_list.conf"
    input_file_handler = open(trim_conf_file)
    trim_list = []
    for line in input_file_handler.readlines():
	if line :
	    trim_list.append(line.decode("utf-8"))
    input_file_handler.close()
    return trim_list;

def deal_data_source(config, type):
    print "deal_%s_source" % (type)
    source_num=config.get(type+"_source", "source_num")
    print source_num
    for i in xrange(int(source_num)):
        print config.get(type+"_source", "get_info"+str(i))

 #   os.system("")

#def deal_toplist_source():

def get_raw_movie_from_db():
    #fake data for now
    trim_list = get_trim_list()
    raw_movie_list = []
    for i in xrange(5):
	raw_movie_data_dict={}
#        raw_movie_data_dict["idx"] = i;
	raw_movie_data_dict["id"] = i;
	raw_movie_data_dict["movie_name"] = "gravity "+trim_list[i];
	raw_movie_data_dict["trim_name"] = ""
	raw_movie_data_dict["poster"] = "www.poster_url.com"
	raw_movie_data_dict["num_fromsite"] = 2000+i
	raw_movie_data_dict["type"] = 0
	raw_movie_data_dict["site_src"] = 0
	raw_movie_data_dict["play_src_url"] = "www.play_url.com"
	raw_movie_data_dict["date"] = time.strftime("%Y%m%d")
	raw_movie_list.append(raw_movie_data_dict)
    for i in xrange(5,10):
	raw_movie_data_dict={}
#        raw_movie_data_dict["idx"] = i;
	raw_movie_data_dict["id"] = i;
	raw_movie_data_dict["movie_name"] = "holmes "+trim_list[i];
	raw_movie_data_dict["trim_name"] = ""
	raw_movie_data_dict["poster"] = "www.poster_url.com"
	raw_movie_data_dict["num_fromsite"] = 2000+i
	if i>5 and i<8:
   	    raw_movie_data_dict["type"] = 0
	    raw_movie_data_dict["site_src"] = 0
	else:
	    raw_movie_data_dict["type"] = 1
	    raw_movie_data_dict["site_src"] = 1
	raw_movie_data_dict["play_src_url"] = "www.play_url.com"
	raw_movie_data_dict["date"] = time.strftime("%Y%m%d")
	raw_movie_list.append(raw_movie_data_dict)
    site_weight_list=[{"site_id":0, "site_weight":5}, {"site_id":1, "site_weight":2}]
    return raw_movie_list, site_weight_list

def trim_movie_name(raw_data, trim_list):
    for i in xrange(len(raw_data)):
        temp_name = raw_data[i]["movie_name"]
	for j in xrange(len(trim_list)):
            trimed = temp_name.replace(trim_list[j],' ')
	    temp_name = trimed
	raw_data[i]["trim_name"] = trimed.rstrip(' ')
    return raw_data

def check_duplicate_trim_name(name_list, check_name):
    flag = 0
    if check_name in name_list:
        print "%s is in name_list" % (check_name)
    else:
        #print "add %s to name_list" % (check_name)	
        name_list.append(check_name)
	flag = 1 
    #print name_list
    return name_list, flag

def get_idx(organize_list, check_name):
    for i in xrange(len(organize_list)):
        if check_name == organize_list[i]["trimed_movie_name"]:
            #return organize_list[i]["idx"]
            return i

def organize_trim_key(trim_data, organize_list):
    #generate a list with trim_name as the key
    name_list=[]
    for i in xrange(len(trim_data)):
        organize_sub_dict={}
        organize_sub_dict["trimed_movie_name"] = trim_data[i]["trim_name"]
	organize_sub_dict["trimed_movie_info"] = []
        base_item_dict={}
	base_item_dict["id"] = trim_data[i]["id"]
	base_item_dict["movie_name"] = trim_data[i]["movie_name"]
	base_item_dict["type"] = trim_data[i]["type"]
	base_item_dict["site_src"] = trim_data[i]["site_src"]
	base_item_dict["num_fromsite"] = trim_data[i]["num_fromsite"]
        name_list, dup_check_flag = check_duplicate_trim_name(name_list, organize_sub_dict["trimed_movie_name"])
	if dup_check_flag == 1:
            # add new trim name to organize_list, whole new organize_sub_dict["trimed_movie_name"] and ["trimed_movie_info"]
	    organize_sub_dict["trimed_movie_info"].append(base_item_dict)
	    organize_list.append(organize_sub_dict)
        elif dup_check_flag == 0:
            # trim name already exist, add base_item_dict to organize_sub_dict["trimed_movie_info"]
            idx_exist = get_idx(organize_list, organize_sub_dict["trimed_movie_name"])
	    organize_list[idx_exist]["trimed_movie_info"].append(base_item_dict)
    return organize_list

def get_site_weight(site_src_id, site_weight_list):
    for i in xrange(len(site_weight_list)):
        if site_src_id == site_weight_list[i]["site_id"]:
            return site_weight_list[i]["site_weight"]

def get_movie_sum_weight(list_to_sum, site_weight_list):
    sum = 0
    for i in xrange(len(list_to_sum)):
        sum = list_to_sum[i]["num_fromsite"] * get_site_weight(list_to_sum[i]["site_src"], site_weight_list)
    return sum

def first_adjust_weight(first_adjust_list, site_weight_list):
    result_list=[]
    for i in xrange(len(first_adjust_list)):
        temp_dict={}
        temp_dict["trim_name"] = first_adjust_list[i]["trimed_movie_name"]
	temp_dict["first_adjust_weight"] = get_movie_sum_weight(first_adjust_list[i]["trimed_movie_info"], site_weight_list)
        result_list.append(temp_dict)
    return result_list

def insert_sort(ori_list):
#{'first_adjust_weight': 4018, 'trim_name': u'holmes'}
    for j in xrange(1, len(ori_list)):
        key=ori_list[j]["first_adjust_weight"]
        key_name=ori_list[j]["trim_name"]
	i=j-1
        while i>-1 and ori_list[i]["first_adjust_weight"]<key:
            ori_list[i+1]["first_adjust_weight"]=ori_list[i]["first_adjust_weight"]
	    ori_list[i+1]["trim_name"]=ori_list[i]["trim_name"]
	    i=i-1
        ori_list[i+1]["first_adjust_weight"]=key
	ori_list[i+1]["trim_name"]=key_name
    return ori_list

def main():
    global_config = get_global_conf()
    deal_data_source(global_config, "online")
    raw_data, site_weight = get_raw_movie_from_db()
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


if __name__ == '__main__':
    main()



