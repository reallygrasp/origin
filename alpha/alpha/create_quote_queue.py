# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 23:35:57 2016

@author: zxz
"""
from __future__ import  print_function
import threading
import Queue
import MySQLdb as mdb
import pandas as pd
from alpha.quote.factor import Factor
from time import ctime,sleep
import pdb
import sys

class Fetch_Quote_Thread(threading.Thread):
    def __init__(self,func_fetch,code,starttime,endtime):
        threading.Thread.__init__(self)
        self.func_fetch=func_fetch
        self.code=code
        self.starttime=starttime
        self.endtime=endtime
        

        print(ctime(),'innitiating fetch_quote_thread:',self.code)
    def run(self):
        
        print(ctime(),'thread is going to apply now:',self.code)
        apply(self.func_fetch,(self.code,self.starttime,self.endtime,))
        
class Push_Quote_Thread(threading.Thread):
    def __init__(self,func_push):
        threading.Thread.__init__(self)
        self.func_push=func_push
        self.quote_obj=quote_queue.get().values()[0]
        
    def run(self):
        #pdb.set_trace()
        
        apply(self.func_push,(self.quote_obj,))
        
quote_queue=Queue.Queue(100)

def fetch_quote(code,starttime,endtime):
    global quote_queue
    try:
        each_quote=Factor(code,starttime,endtime)
        #pdb.set_trace()
        print('@'*100)
        print(code,'have susccessfully got Factor instance')
        print('@'*100)
    except Exception,e:
        print(ctime(),code,'fetch_quote initiating Factor failed:',e)
        return
    #pdb.set_trace()
    print(ctime(),'calling fetch_quote function:',code)
    #pdb.set_trace()
    if each_quote.data.empty:
        return
    try:
        each_quote.Cal_pe()
        #pdb.set_trace()
        each_quote.Add_margin()
        #pdb.set_trace()
        each_quote.Add_date()
        each_quote.Add_code_Abbr()
        quote_dict={}
        quote_dict[code]=each_quote
        quote_queue.put(quote_dict)
        print('queue size now is :',quote_queue.qsize())
        
    except Exception,e:
        print(code,'getting factors failed:',e)
def push_quote(quote_obj):
    #pdb.set_trace()
    code=quote_obj.data.stockCode[0]
    param_create=('sh'+code)if int(code)>=600000 else ('sz'+code)
    try:
        conn=mdb.connect(host='localhost',user='root',passwd='Free.Pursue-2012',db='alpha',charset='utf8')
        cur=conn.cursor()
        conn.select_db('alpha')
    except Exception,e:
        print('cannot connect mysqldb for:',e)
    try:
        sql_create="""create table %s(open decimal(5,3),high decimal(5,3),
        close decimal(5,2),low decimal(5,2),volume float,price_change decimal(5,2),
        p_change decimal(5,2),ma5 decimal(6,3),ma10 decimal(6,3),ma20 decimal(6,3),
        v_ma5 float,v_ma10 float,v_ma20 float,turnover decimal(4,2),
        eps decimal(6,3),roe decimal(6,3),net_profits float,pe float,
        rzye bigint,rzmre bigint,rqyl bigint,rqmcl bigint,date date not null unique,
        stockCode char(6),securityAbbr varchar(20),primary key(date)) 
        default charset=utf8;"""%param_create
        print('$'*100)
        print('已经成功生产MYSQL表:',param_create)
        print('$'*100)
        cur.execute('drop table if exists %s;'%param_create)
        cur.execute(sql_create)
        conn.commit()
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
    param_insert=quote_obj.data.values
    sql_insert="""insert into {0} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""".format(param_create)
    #pdb.set_trace()
    for line in param_insert:
        #pdb.set_trace()
        cur.execute(sql_insert,tuple(line))
        #pdb.set_trace()
    conn.commit()
    cur.close()
    conn.close()
def main():
    code_list=[]
    code_name=pd.read_csv(r'/home/site/AlphaStrategy/alpha/alpha/code_name.csv',encoding='utf-8')
    code_name.columns=['code','name']
    for each in code_name.code:
        code_list.append('0'*(6-len(str(int(each))))+str(int(each)))
    print(code_list[1900:1910])

    thread_quote_list=[]
    for each_code in code_list[0:50]:
        print('thread quote is building:',each_code)
        #pdb.set_trace()
        thread_quote=Fetch_Quote_Thread(fetch_quote,each_code,starttime='2013-03-28',endtime='2016-03-28')
        thread_quote_list.append(thread_quote)
        #pdb.set_trace()
        
    
    for j in range(len(thread_quote_list)):
        print(ctime(),'thread quote is going to start:',thread_quote_list[j])
        #pdb.set_trace()
        thread_quote_list[j].start()
        
    sleep(10)
    for k in range(len(thread_quote_list)):
        #pdb.set_trace()
        
        thread_quote_list[k].join()
        while not quote_queue.empty():
            thread_push=Push_Quote_Thread(push_quote)
            thread_push_list=[]
            thread_push_list.append(thread_push)
            for t in thread_push_list:
                t.start()
                t.join()
    
        
if __name__=='__main__':
    main()
    print('#'*100)
    print('all done!')
    print('#'*100)     
