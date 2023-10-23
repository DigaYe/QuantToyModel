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


#%% MomentumRSI Trading Signal 

class MomentumRSI(BackTestSA):

    def __init__(self, csv_path, date_col, max_holding, ub_mult,
                 lb_mult, rsi_window, rsi_long=30, rsi_short=70,
                 ma_long = 200, ma_short=50):

        super().__init__(csv_path, date_col, max_holding)

        self.ub_mult = ub_mult
        self.lb_mult = lb_mult

        #rsi parameters
        self.rsi_window = rsi_window
        self.rsi_long = rsi_long
        self.rsi_short = rsi_short

        #moving average parameters
        self.ma_long = ma_long
        self.ma_short = ma_short


    def calculate_rsi(self):
        '''
        calculates RSI based on the window argument passed into constructor
        https://en.wikipedia.org/wiki/Relative_strength_index
        '''
        df = self.dmgt.df
        #creat change column
        df['change'] = df.close.diff()
        df['U'] = [x if x > 0 else 0 for x in df.change]
        df['D'] = [abs(x) if x < 0 else 0 for x in df.change]
        df['U'] = df.U.ewm(span=self.rsi_window,
                           min_periods=self.rsi_window-1).mean()
        df['D'] = df.D.ewm(span=self.rsi_window,
                           min_periods=self.rsi_window - 1).mean()

        df['RS'] = df.U / df.D
        df['RSI'] = 100 - 100/(1+df.RS)
        df.drop(['change', 'U', 'D', 'RS'],
                axis=1, inplace=True)

    def calculate_ma(self):
        '''
        calculates two expontential movings averages, based on arguments passed
        into construtor
        '''
        df = self.dmgt.df
        df['ma_long'] = df.close.ewm(span=self.ma_long,
                                     min_periods=self.ma_long-1).mean()
        df['ma_short'] = df.close.ewm(span=self.ma_short,
                                      min_periods=self.ma_short - 1).mean()


    def generate_signals(self):
        df = self.dmgt.df
        self.calculate_ma()
        self.calculate_rsi()
        df.dropna(inplace=True)
        # 1 if rsi < 30 & ma_short > ma_long, 0 otherwise
        df['longs'] = ((df.RSI < self.rsi_long) & (df.ma_short > df.ma_long))*1
        # -1 if rsi > 70 & ma_short < ma_long, 0 otherwise
        df['shorts'] = ((df.RSI > self.rsi_short) & (df.ma_short < df.ma_long))*-1
        df['entry'] = df.longs + df.shorts
        df.dropna(inplace=True)

    def save_backtest(self, instrument):
        '''
        :param instrument: ETH, BTC for Ethereum and Bitcoin
        saves backtest to our backtests folder
        '''
        strat_name = self.__class__.__name__
        tf = self.dmgt.timeframe
        self.dmgt.df.to_csv(f"data/backtests/{strat_name}_{tf}-{instrument}.csv")
