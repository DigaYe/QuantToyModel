# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:59:10 2023

@author: yej
"""
#%%
import datetime as dt
import pandas_ta as ta
import pandas as pd
import yfinance as yf
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from xbbg import blp
import backtesting
# Set up for plot
backtesting.set_bokeh_output(notebook=False)
#%% Data Collector
class AssetData:
    def __init__(self, ticker, start_date, 
                 end_date = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d")):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date 

    def get_yf_data(self):
        df = yf.download(self.ticker, start = self.start_date, end = self.end_date)
        return df
    
    def get_bbg_data(self, fields = ['Open', 'High', 'Low', 'Last Price','Volume'], transform = True):
        df = blp.bdh(tickers=self.ticker, flds = fields, start_date= self.start_date, end_date=self.end_date)
        if transform:
            df = df[self.ticker].rename(columns = {'Last Price':"Close"}, errors="raise")
            df.index = pd.to_datetime(df.index)
        return df



#%% RSI Signals

class RSI:
    def __init__(self, data, window = 14, ewm = False,xa = 70, xb= 30):
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
    

    
class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    
    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if crossover(self.rsi, self.upper_bound): # true if rsi > upperbound - sell signal
            self.position.close()
        elif crossover(self.lower_bound, self.rsi): # true if lower_bound > rsi - buy signal 
            self.buy()
            
#%% Paramater Optimizaion 
def optim_func(series):
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']
   
#%% Run Strategy

# Get Data
ticker = "SPX Index"
data = AssetData(ticker, "2018-10-21").get_bbg_data()

# Run BackTesting
bt = Backtest(data, RsiOscillator, cash=10_000, commission=.002)
stats = bt.run()
bt.plot()

# Paramater Optimizaion 
stats = bt.optimize(
        upper_bound = range(50,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,30,2),
        maximize='Sharpe Ratio')

#%% Get Trade Data
all_trade_data = stats['_trades']










