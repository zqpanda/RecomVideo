#!/home/hao123/tools/python/bin/python2.7
# -*- coding:utf-8 -*-
import ConfigParser
import MySQLdb as mdb
import time,sys

class MySQLDB:
    def __init__(self,host,user,password,port,charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        try:
            self.conn=mdb.connect(host=self.host,user=self.user,passwd=self.password,port=self.port)
            self.conn.set_character_set(self.charset)
            self.cur=self.conn.cursor()
        except mdb.Error as e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    def selectDb(self,db):
        try:
            self.conn.select_db(db)
        except mdb.Error as e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    def query(self,sql):
        try:
            n=self.cur.execute(sql)
            return n
        except mdb.Error as e:
            print sql
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    def queryRow(self,sql):
        self.query("set names utf8")
        self.query(sql)
        result = self.cur.fetchone()
        return result
    
    def queryAll(self,sql):
        self.query("set names utf8")
        self.query(sql)
        result=self.cur.fetchall()
        desc=self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0,len(inv)):
                _d[desc[i][0]]=str(inv[i])
            d.append(_d)
        return d
    def insert(self,p_table_name,p_data):
        for key in p_data.keys():
            p_data[key] = mdb.escape_string(p_data[key])
            p_data[key] = "'"+p_data[key]+"'"
        key = ','.join(p_data.keys())
        value = ','.join(p_data.values())
        real_sql = "INSERT INTO " + p_table_name + "(" +key + ") VALUES (" + value + ")"
        self.query("set names utf8")
        return self.query(real_sql)
    def escape_string(self,item):
        return mdb.escape_string(item)
    def commit(self):
        self.conn.commit()
    def close(self):
        self.cur.close()
        self.conn.commit()

def read_conf(conffile):
    cf = ConfigParser.ConfigParser()
    cf.read(conffile)
    db_conf = {
        'host' : cf.get('db','db_host'),
        'user' : cf.get('db','db_user'),
        'passwd' : cf.get('db','db_pass'),
        'port' : cf.getint('db','db_port'),
        'charset' : cf.get('db','db_charset')
    }
    return db_conf

def main():
    db_conf = read_conf('../conf/db.conf')
    MyDb = MySQLDB(db_conf['host'],db_conf['user'],db_conf['passwd'],db_conf['port'])
    db_name = "video_recom_ar"
    MyDb.selectDb(db_name)
    sql = "select raw_title from movie_raw_data"
    result = MyDb.queryAll(sql)
    for line in result:
        print 'Raw Title: ' + line['raw_title']
    MyDb.close()

if __name__ == '__main__':
    main()
