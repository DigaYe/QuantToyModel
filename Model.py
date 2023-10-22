#%% Import Package
import numpy as np
import datetime as dt
from xbbg import blp
import plotly as px
import yfinance as yf

#%% Individual Asset
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
    
    def std(self, adj = False, crypto = False):
        returns = self.simple_returns(adj).mul(100)
        trading_days  = 252
        std = returns.describe().T.loc["std"]
        std = std*np.sqrt(trading_days)
        return std
    
    
    
    
#%% Test Asset
spy = Asset('SPX Index', '2020-10-01')
spy_df = spy.get_bbg_data(fields=['Last Price', 'High'])


