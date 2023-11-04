# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:56:55 2023

@author: yej
"""
#%% Packages
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
from xbbg import blp
import yfinance as yf
from pandas.tseries.offsets import MonthEnd
import pandas_ta
import matplotlib.pyplot  as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#%% Data Class
class AssetData:
    def __init__(self, ticker, start_date, 
                 end_date = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d")):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date 

    def get_yf_data(self):
        df = yf.download(self.ticker, start = self.start_date, end = self.end_date)
        return df
    
    def get_bbg_data(self, fields = ['Last Price']):
        df = blp.bdh(tickers=self.ticker, flds = fields, start_date= self.start_date, end_date=self.end_date)
        df = df[ticker]
        df.index.name = ticker
        return df

#%% RSI Trading Signal 
class RSI:
    def __init__(self, data, window = 14, ewm = False,xa = 80, xb= 20):
        self.data = data
        self.window = window
        self.ewm = ewm
        self.xa = xa
        self.xb = xb

    
    def cal_rsi(self):
        '''
        calculates RSI based on the window argument passed into constructor
        https://en.wikipedia.org/wiki/Relative_strenselgth_index
        '''
        #creat change column
        df = self.data.copy()
        df["Change"] = df.diff()
        df["Change_up"] = [x if x > 0 else 0 for x in df["Change"]]
        df["Change_down"] = [x if x < 0 else 0 for x in df["Change"]]
        
        
        df["Avg_up"] = df["Change_up"].rolling(self.window).mean()
        df["Avg_down"] = df["Change_down"].rolling(self.window).mean().abs()

        df['RSI'] = 100 * df["Avg_up"] / (df["Avg_up"] + df["Avg_down"] )
        return df
    
    def cal_signals(self):
        df = self.cal_rsi().copy()
        df["Buy_" + str(self.xb)] = [1 if x < self.xb else 0 for x in df["RSI"]]
        df["Sell_" + str(self.xa)] = [-1 if x > self.xa else 0 for x in df["RSI"]]
        df["Position"] =df["Buy" + str(self.xb)] + df["Sell_" + str(self.xa)]
        return df

    def plot_signals(self, datapoints = 300):
       
        plot_data = self.cal_signals()[-datapoints:]
        plt.figure(figsize=(10, 7))
        plt.title('Long and Short Signal', fontsize=14)
        plt.xlabel('Date')
        plt.ylabel('Last Price')
        plt.plot(plot_data['Last Price'], label='Close')


        plt.plot(plot_data[(plot_data['Position'] == 1)]["Last Price"], '^', label='Buy Signal', ms=15, color='green')
        plt.plot(plot_data[(plot_data['Position'] == -1)]["Last Price"], '^',label='Short Signal', ms=15, color='red')
        plt.legend()

        plt.show()
        
    def cal_return(self, fig = True):
        df = self.cal_signals()
        df["Return"] = df["Last Price"].pct_change()
        df['Strategy_returns'] = df['Return'] * df['Position'].shift(1)
        df['Cumulative_return'] = (df['Strategy_returns'] + 1).cumprod()
        if fig:
            df['Cumulative_return'].plot(figsize=(10, 7))
            plt.title('Cumulative Strategy Returns')
            plt.show()
        return df
        
    
#%% Run
ticker = "SPX Index"
data = AssetData(ticker, "2023-10-21").get_bbg_data()

#%%
spx = RSI(data)
spx.plot_signals()
df= spx.cal_return()




