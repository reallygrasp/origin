# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 20:53:57 2016

@author: zxz
"""
from __future__ import print_function
import pandas as pd
from alpha.quote.quote import Quote
from alpha.margin.margin import Margin
from time import ctime,sleep
from pandas import DataFrame
class Factor(Quote):
    def __init__(self,code,starttime,endtime):
        self.code=code
        self.starttime=starttime
        self.endtime=endtime
        
        #self.data=DataFrame()
        super(Factor,self).__init__(code=self.code,starttime=self.starttime,endtime=self.endtime)
        self.Fetch_Data()
        
        print(ctime(),':Factor initiated code:',self.code)
        
        
    def Cal_pe(self):
        try:
            if self.data is not None:
                self.data['pe']=self.data['close']/self.data['eps']
            else:
                return
        except Exception,e:
            print('cal_pe error,reason:',e)
        
    def Cal_pb(self):
        try:
            if self.data is not None:
                self.data['pe']=self.data['close']/self.data['eps']
            else:
                return
        except Exception,e:
            print('cal_pb error,reason:',e)
        return
    def Add_date(self):
        try:
            if self.data is not None:
                self.data['date']=list(self.data.index)
            else:
                return
        except Exception,e:
            print('Add_date error,reason:',e)
    def Add_code_Abbr(self):
        try:
            if self.data is not None:
                code_abbr=pd.read_csv(r'/home/site/AlphaStrategy/alpha/alpha/code_name.csv',encoding='utf-8')
                code_abbr.columns=['code','name']
                self.data['stockCode']=self.code
                self.data['securityAbbr']=code_abbr[code_abbr.code==int(self.code)].iloc[0][1]
            else:
                return
        except Exception,e:
            print(self.code,'add_code_Abbr error:',e)
    def Add_margin(self):
        if self.data is None:
            return
        margin=Margin(self.code,self.starttime,self.endtime)
        margin.Get_margin()
        if len(margin.margin)==0:
            print(self.code,'cannot margin and short')
            
            self.data['rzye']=[1]*len(self.data)
            self.data['rzmre']=[1]*len(self.data)
            self.data['rqyl']=[1]*len(self.data)
            self.data['rqmcl']=[1]*len(self.data)
            return
        else:
            
            self.data['rzye']=list(margin.margin.rzye)
            self.data['rzmre']=list(margin.margin.rzmre)
            self.data['rqyl']=list(margin.margin.rqyl)
            self.data['rqmcl']=list(margin.margin.rqmcl)
            
    def Plot_quote(self):
        try:
            if self.data is not None:
                self.data[['close','pe']].plot()
            else:
                return
        except Exception,e:
            print('ploting error,reason:',e)
if __name__=='__main__':
    
    asd=Factor('002333',starttime='2016-03-20',endtime='2016-03-28')
    asd.Cal_pe()
    asd.Add_margin()
    asd.Add_date()
    asd.Add_code_Abbr()
    print('*'*100)
    print(asd.data)
    print('*'*100)
    #print(gzmt.data.tail())
    
        
