# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:12:05 2016

@author: zxz
"""
from __future__ import print_function
import tushare as ts
from pandas import DataFrame
from alpha.quote.quote import Quote
import pandas as pd
import pdb
import threading
from time import ctime

margin_dict={}
margin_lock=threading.RLock()
class Get_szMargin_Thread(threading.Thread):
    def __init__(self,func,code,date):
        threading.Thread.__init__(self)
        self.func=func
        self.code=code
        self.date=date
    def run(self):
        apply(self.func,(self.code,self.date))

def Get_szMargin(code,date):
    global margin_dict
    global margin_lock
    each_margin=ts.sz_margin_details(date)
    if each_margin.empty:
        return
    #pdb.set_trace()
    else:
        if code not in list(each_margin.stockCode):
            return
        else:
            try:
                margin_lock.acquire()
                margin_dict[date]=each_margin[each_margin.stockCode==code]
                margin_lock.release()
            except Exception,e:
                print('geting szmargin failed for:',e)
    
class Margin(Quote):
    def __init__(self,code,starttime,endtime):
        self.starttime=starttime
        self.endtime=endtime
        self.code=code
        super(Margin,self).__init__(code,starttime,endtime)
        #self.Fetch_Data()
        self.margin=DataFrame()
        print(ctime(),':Margin initiated:',code)
        
    def Get_Margin_sz(self):
        thread_list=[]
        for i in range(len(self.data.index)):
            t=Get_szMargin_Thread(Get_szMargin,self.code,self.data.index[i])
            thread_list.append(t)
        for i in range(len(self.data.index)):
            thread_list[i].start()
        for i in range(len(self.data.index)):
            thread_list[i].join()
    def Get_margin(self):
        try:
            if int(self.code)>60000 and int(self.code)<610000:
                self.margin=ts.sh_margin_details(start=self.starttime,end=self.endtime,symbol=self.code).sort_values(by='opDate',ascending=True)
            elif int(self.code)>0 and int(self.code)<3000:
                self.Get_Margin_sz()
                print(sorted(margin_dict.keys()))
                margin_list=[margin_dict[k] for k in sorted(margin_dict.keys())]
                self.margin=pd.concat(margin_list)
                
                
                #margin_list=[]
                #for date in self.data.index:
                #    each_margin=ts.sz_margin_details(date)
                #    each_margin=each_margin[each_margin.stockCode==self.code]
                #    margin_list.append(each_margin)
                #self.margin=pd.concat(margin_list)
            else:
                print('code error')
        except Exception,e:
            print('getting margin failed,reason:',e)
if __name__=='__main__':
    code_list=['002337']
    margin_list=[]
    for code in code_list:
        margin_list.append(Margin(code,'2015-01-01','2015-01-10'))
    for mar in margin_list:
        mar.Get_margin()
        print('*'*100)
        print(mar.margin)