#%% Import Package
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
from xbbg import blp
import yfinance as yf

#%% Cast into a class
class indexdata:
    def __init__(self, ticker, close, volume):
        self.ticker = ticker
        self.close = close
        self.volume = volume
# method - technical indicator
msft = yf.Ticker("MSFT")
#%% Get Country Data
startdate = '2010-10-10'
enddate = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d")
index_list = ['MXUS Index', 'MXJP Index', 'MXEU Index', 'MXCN Index']

# US, Japan, Europe, China
country_index_data = blp.bdh(tickers=index_list, 
                             flds=['TOT_RETURN_INDEX_GROSS_DVDS'],
                             start_date= startdate, 
                             end_date=enddate)


# Clean up a df


#%% Get Technical Indicator Data

# Simple Moving Average 
def SMA(data, ndays): 
    SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = 'SMA') 
    data = data.join(SMA) 
    return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
    EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                 name = 'EWMA_' + str(ndays)) 
    data = data.join(EMA) 
    return data

# Relative Strength Index
def rsi(close, periods = 14):
    
    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


# Bollinger Band
def BBANDS(data, window = n):
    MA = data.Close.rolling(window=n).mean()
    SD = data.Close.rolling(window=n).std()
    data['MiddleBand'] = MA
    data['UpperBand'] = MA + (2 * SD) 
    data['LowerBand'] = MA - (2 * SD)
    return data
 

#%% Return Model 






