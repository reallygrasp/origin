# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 22:02:13 2016

@author: zxz
"""
from __future__ import print_function
import os
import pandas as pd
from pandas import DataFrame
from time import ctime
class Reports(object):
    def __init__(self,code):
        self.code=int(code)
        self.reports=DataFrame()
        print(ctime(),':Reports initiated:',self.code)
        
    @staticmethod
    def Fetch_Reports_All():
        reports_file_list=[]
        for (dirpath,dirnames,filenames) in os.walk(r'/home/site/AlphaStrategy/alpha/alpha/reports'):
            for file in filenames:
                try:
                    reports_file_list.append(dirpath+'/'+file)
                except Exception,e:
                    print('lising reports.csv error:',e)
                    
        reports_list=[]
        reports_all=pd.DataFrame()
        for report_file in reports_file_list:
            try:
                curent_report=pd.read_csv(report_file)
            except Exception,e:
                print('reading reports failed:',e)
            curent_report['report_date']=report_file[-10:-6]+'-'+curent_report['report_date']
            reports_list.append(curent_report)
            curent_report=0
        reports_all=pd.concat(reports_list)
        reports_all=reports_all[reports_all.eps.notnull()]
        reports_all=reports_all[reports_all.roe.notnull()]
        #reports_all=reports_all[reports_all.bvps.notnull()]
        #reports_all=reports_all[reports_all.net_profits.notnull()]
        reports_all.drop_duplicates(subset=['code','report_date'])
        return reports_all
    @staticmethod
    def Fesports_To_Csv():
        reports=Reports.Fetch_Reports_All()
        reports.to_csv(r'/home/site/AlphaStrategy/alpha/alpha/reports_all.csv',ignore_index=True)

    def Get_Report_Individual(self):
        reports=self.Fetch_Reports_All()
        each_report=reports[reports.code==self.code]
        if len(each_report)==0:
            return DataFrame()
        else:
            self.reports=each_report
        self.reports=self.reports.drop_duplicates(['report_date']).dropna(axis=1,how='all')
        return self.reports.sort_values(by='report_date',ascending=True)
if __name__=="__main__":
    sh600518=Reports('600518')
    sh600518_report=sh600518.Get_Report_Individual()
    print(sh600518_report)
