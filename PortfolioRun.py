# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 11:38:41 2023

@author: yej
"""
#%% Import Package
import numpy as np
import datetime as dt
import random 

#%% Multi-Asset Portfolio
class Portfolio:
    def __init__(self, assets, start_date, weights = None, end_date = dt.date.today().strftime('%Y-%m-%d')):
        self.assets = assets
        self.start_date = start_date
        self.end_date = end_date
        
        if weights is not None:
            self.weights = np.array(weights)
        else:
            self.weights = self.generate_random_weights()
            
    def generate_random_weights(self):
    # Generate random weights that add up to 1 and round to 1 digit
        weights = [round(random.random(), 1) for _ in range(len(self.assets))]
        total_weight = sum(weights)
        return np.array([round(weight / total_weight, 1) for weight in weights])
  
    def portfolio_returns(self, adj = False, cum = False):
        returns = self.simple_returns(adj, cum)
        portfolio_returns = (returns*self.weights).sum(axis=1)
        return portfolio_returns
    
#%% Collect Data with Input 
assets = ['SPY', 'AAPL', 'META']
start_date = '2017-01-01'
weights = [0.4, 0.3, 0.3]

port = Portfolio(assets, start_date, weights)