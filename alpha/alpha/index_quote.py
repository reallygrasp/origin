# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 20:41:20 2016

@author: zxz
"""
from __future__ import print_function
import pandas as pd
import MySQLdb as mdb
import tushare as ts
import pdb
if __name__=='__main__':
    hs300_data=ts.get_hist_data('hs300',start='2014-07-28',end='2016-07-28').sort_index()
    hs300_data['date']=hs300_data.index
    #pdb.set_trace()
    index_quote='hs300'
    try:
        conn=mdb.connect(host='localhost',user='root',passwd='Free.Pursue-2012',db='alpha',charset='utf8')
        cur=conn.cursor()
        conn.select_db('alpha')
    except Exception,e:
        print('cannot connect mysqldb for:',e)
    try:
        sql_create="""create table %s(open decimal(7,3),high decimal(7,3),
        close decimal(7,3),low decimal(7,3),volume float,price_change decimal(7,3),
        p_change decimal(7,3),ma5 decimal(7,3),ma10 decimal(7,3),ma20 decimal(7,3),
        v_ma5 float,v_ma10 float,v_ma20 float,date date not null unique,primary key(date)) 
        default charset=utf8;"""%index_quote
        
        cur.execute('drop table if exists %s;'%index_quote)
        cur.execute(sql_create)
        conn.commit()
        print('$'*100)
        print('已经成功产生MYSQL表:',index_quote)
        print('$'*100)
    except Exception,e:
        print('cannnot create table for:',e)
    cur.close()
    conn.close()
    try:
        conn=mdb.connect(host='localhost',user='root',passwd='Free.Pursue-2012',db='alpha',charset='utf8')
        cur=conn.cursor()
        conn.select_db('alpha')
    except Exception,e:
        print("cannot connect mysqldb for:",e)
    param_insert=hs300_data.values
    
    sql_insert="""insert into {0} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""".format(index_quote)
    #pdb.set_trace()
    try:
        for line in param_insert:
        
        #pdb.set_trace()
            cur.execute(sql_insert,tuple(line))
    except Exception,e:
        print(index_quote,'sql insert failed for:',e)
        #pdb.set_trace()
    conn.commit()
    cur.close()
    conn.close()