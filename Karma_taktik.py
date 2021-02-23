exchange_public_key = 'n7YeAc1LoHG28qbzAuSWS92m8ZX9uxtg4qo2fPpIehnMkWqmGPwbEove2pNVar4Q'
exchange_secret_key = 'WI1CWGX7EweNKpxHntj2UdaENzrzMuEm6CLFuoxHK6adyi3B4YZl6XvLnqpdOOsZ'


import psycopg2
import binance
import requests
import config
import csv

import backtrader as bt
from matplotlib.dates import warnings

class Karma_taktik(bt.Strategy):
    params = (
    # Standard MACD Parameters
    ('atrperiod', 14),  # ATR Period (standard)
    ('atrdist', 3.0),   # ATR distance for stop price
    ('smaperiod', 30),  # SMA Period (pretty standard)
    ('dirperiod', 10),)  # Lookback period to consider SMA trend direction
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        
        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def __init__(self):
        self.ema1 = bt.talib.EMA(self.data, timeperiod = 9)
        self.ema2 = bt.talib.EMA(self.data, timeperiod = 13)
        self.ema3 = bt.talib.EMA(self.data, timeperiod = 26)
        

        self.crossover1 = self.ema1 - self.ema3
        self.crossover2 = self.ema2 - self.ema3

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)
        self.rsi = bt.talib.RSI(self.data, period=14)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order
    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
           pclose = self.data.close[0]
           if pclose > self.ema3:
                if self.ema2 > pclose > self.ema3:
                        self.order = self.buy()
                        pdist = self.atr[0] * self.p.atrdist
                        self.pstop = self.data.close[0] - pdist
                        self.target = self.data.close[0] + (3*self.atr[0])

        elif self.position:
            if self.data.close[0] == self.target:
                self.close()
            else:  # in the market
                pclose = self.data.close[0]
                pstop = self.pstop
                if pclose < pstop:
                    self.close()  # stop met - get out
                else:
                    pdist = self.atr[0] * self.p.atrdist
                    # Update only if greater than
                    self.pstop = max(pstop, pclose - pdist)
    