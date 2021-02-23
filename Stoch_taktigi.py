exchange_public_key = 'n7YeAc1LoHG28qbzAuSWS92m8ZX9uxtg4qo2fPpIehnMkWqmGPwbEove2pNVar4Q'
exchange_secret_key = 'WI1CWGX7EweNKpxHntj2UdaENzrzMuEm6CLFuoxHK6adyi3B4YZl6XvLnqpdOOsZ'


import psycopg2
import binance
import requests
import config
import csv

import backtrader as bt
from matplotlib.dates import warnings

class Stoch_taktigi(bt.Strategy):
    params = (('period', 14), ('pfast', 3), ('pslow', 3), ('upperLimit', 80),
             ('lowerLimit', 20), ('stop_pips', .002))

    def __init__(self):
        self.stochastic = bt.indicators.Stochastic(self.data, period=self.params.period, period_dfast=self.params.pfast, period_dslow=self.params.pslow, 
            upperband=self.params.upperLimit, lowerband=self.params.lowerLimit)
        
    def next(self):

        if not self.position:
            if self.stochastic.lines.percD[-1] <= 20 and self.stochastic.lines.percD[0] >= 20:
                self.buy()
        if self.position:
            if (self.stochastic.lines.percD[0] >= 70):
                self.close()