# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:40:25 2023

@author: yej
"""

#%% Import Package
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
from xbbg import blp
import yfinance as yf
from pandas.tseries.offsets import MonthEnd

#%% Get Raw Data
class Asset:
    def __init__(self, ticker, start_date, end_date = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d")):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date 

    def get_yf_data(self):
        df = yf.download(self.ticker, start = self.start_date, end = self.end_date)
        return df
    
    def get_bbg_data(self, fields = ['Last Price']):
        df = blp.bdh(tickers=self.ticker, flds = fields, start_date= self.start_date, end_date=self.end_date)
        return df

    def simple_returns(self, adj = False, cum = False):
            df = self.get_data()
            if adj:
                simple_returns = df["Adj Close"].pct_change().dropna()
            else:
                simple_returns = df["Close"].pct_change().dropna()
            if cum: # cumulate return
                simple_returns = (1 + simple_returns).cumprod() - 1
            return simple_returns
    
    def std(self, adj = False):
        # Market Vol
        returns = self.simple_returns(adj).mul(100)
        trading_days  = 252
        std = returns.describe().T.loc["std"]
        std = std*np.sqrt(trading_days)
        return std
    
    

#%% Construct Technical Indicator

class MA(Asset):
    def __int__(self, period):
        self.period = period
    
    
    def Cal_SMA(self):
        self.get_bbg_data(self)