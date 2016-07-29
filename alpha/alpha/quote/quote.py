# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 00:48:54 2016

@author: zxz
"""
from __future__ import print_function
import tushare as ts
from pandas import DataFrame
from alpha.report.report import *
from time import ctime
class Quote(object):
    def __init__(self,code,starttime,endtime):
        self.code=code
        self.starttime=starttime
        self.endtime=endtime
        self.reports=DataFrame()
        self.report_obj=0
        self.data=DataFrame()
        try:
            self.data=ts.get_hist_data(self.code,self.starttime,self.endtime)
            if self.data is not None:
                self.data=self.data.sort_index()
                print(ctime(),':Quote initiated successful:',self.code)
            else:
                self.data=DataFrame()
                print(ctime(),':Quote initiated failed:',self.code)
        except Exception,e:
            self.data=DataFrame()
            print(ctime(),self.code,'quote initiating error,reason:',e)
        
    def Quote_add_col(self,param):
        if self.data.empty:
            return
        print(self.code,'is calling Quote_add_col and adding param:',param)
        self.reports=self.report_obj.Get_Report_Individual()
        if self.reports.empty:
            self.data.columns.append(param)
        elif param not in self.reports.columns:
            print('cannot add_col:',param)
            return
        else:
            self.data[param]=0
            try:
                for date in self.reports.report_date:
                    report_param=self.reports.loc[self.reports.report_date==date,[param]]
                    self.data.loc[self.data.index>=date,[param]]=report_param.iloc[0][0]
                    
            except Exception,e:
                print('adding %s error,reason:'%param,e)
    def Fetch_Data(self):
        if self.data.empty:
            return
        else:
            self.report_obj=Reports(int(self.code))
            self.Quote_add_col('eps')
            self.Quote_add_col('roe')
            self.Quote_add_col('net_profits')
        #self.Quote_add_eps()
        #self.Quote_add_roe()
        #self.Quote_add_net_profits()
        
if __name__=="__main__":
    sh=Quote('002337','2016-04-01','2016-04-27')
    sh.Fetch_Data()
    print('*'*100)
    print(sh.data)
    print('*'*100)
    