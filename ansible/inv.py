#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
从mysql数据库中读取出ansible的host和group列表，并返回json格式
'''
 
# 加载模块
import MySQLdb
import MySQLdb.cursors
 
try:
    import json
except ImportError:
    import simplejson as json
 
mysql_host = 'localhost'
mysql_db = 'ansible'
mysql_user = 'root'
mysql_pwd = ''
 
 
def DB_connect(sql):
    conn = MySQLdb.connect(host=mysql_host,
                           user=mysql_user,
                           passwd=mysql_pwd,
                           db=mysql_db,
                           port=3306,
                           charset='utf8',
                           connect_timeout=2,
                           cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()  # 提交数据
        return cursor.fetchall()
    except Exception, e:
        conn.rollback()  # 数据回滚
        return "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    conn.close()
 
 
def GetData():
    list = {}
    value = {}
    list["_meta"] = {"hostvars": value}
    sql = 'select * from ansible'  # 查询所有数据
    result = DB_connect(sql)
    for data in result:
        if data['group'] not in list.keys():
        	list[data['group']] = []  # 创建组
        list[data['group']].append(data['hosts'])

        del  data['group']
        value[data['hosts']] = {}
        for key in data:
		if key != 'hosts':
			value[data['hosts']][key] = data[key]
    	
    return json.dumps(list)
 
if __name__ == '__main__':
    print GetData()
