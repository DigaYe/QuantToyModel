#%% Import Package
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
from xbbg import blp
import yfinance as yf
from pandas.tseries.offsets import MonthEnd

#%% Get Country Data
startdate = '2010-10-10'
enddate = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d")
tickers = ['SPX Index']

# US, Japan, Europe, China
data = blp.bdh(tickers=tickers, 
                start_date= startdate, 
                end_date=enddate).fillna(method='ffill')


#%% Get Technical Indicator Data

# Simple Moving Average 
def SMA(data, ndays): 
    data[(data.columns[0][0], "SMA_" + str(ndays))] = data.rolling(ndays).mean()
    return data


# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
    data[(data.columns[0][0], "EWMA_" + str(ndays))] = data.ewm(span = ndays, min_periods = ndays - 1).mean()  
    return data

# Relative Strength Index
def rsi(data, periods = 14):
    data[(data.columns[0][0], "RSI_" + str(periods))] = data.diff()
    close_delta = data[(data.columns[0][0], "RSI_" + str(periods))]

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


#%% Get Technical Indicator
sma = SMA(data, 5)
ema = EWMA(data, 5)
rsi = rsi(data)

#%% Return Model 

#%% Trade Signal 






