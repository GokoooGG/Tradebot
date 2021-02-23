exchange_public_key = 'n7YeAc1LoHG28qbzAuSWS92m8ZX9uxtg4qo2fPpIehnMkWqmGPwbEove2pNVar4Q'
exchange_secret_key = 'WI1CWGX7EweNKpxHntj2UdaENzrzMuEm6CLFuoxHK6adyi3B4YZl6XvLnqpdOOsZ'


import psycopg2
import binance
import requests
import config
import csv

import backtrader as bt
from matplotlib.dates import warnings

class TEMA_taktigi(bt.Strategy): #3EMA
       
    def __init__(self):
        self.ema1 = bt.talib.EMA(self.data, timeperiod = 9)
        self.ema2 = bt.talib.EMA(self.data, timeperiod = 13)
        self.ema3 = bt.talib.EMA(self.data, timeperiod = 26)
        
        self.crossover1 = self.ema1 - self.ema3
        self.crossover2 = self.ema2 - self.ema3


    def next(self):
        if not self.position:
            if self.crossover1 > 0:
                if self.crossover2 > 0:
                    self.buy()

        if self.position:
            if self.crossover1 < 0:
                if self.crossover2 < 0:
                    self.close()
