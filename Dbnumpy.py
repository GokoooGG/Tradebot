##############Ta-Lib kurulumu için https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

##############The base websocket endpoint is: wss://stream.binance.com:9443

exchange_public_key = 'n7YeAc1LoHG28qbzAuSWS92m8ZX9uxtg4qo2fPpIehnMkWqmGPwbEove2pNVar4Q'
exchange_secret_key = 'WI1CWGX7EweNKpxHntj2UdaENzrzMuEm6CLFuoxHK6adyi3B4YZl6XvLnqpdOOsZ'


import psycopg2
import binance
import requests
import config
import csv


##############DATABASE BAGLANTISI
conn = psycopg2.connect("dbname=Binance user=postgres password=3210")
curr = conn.cursor()
print( conn.get_dsn_parameters() )

curr.close()
conn.close()

##############BİNANCE APİ BAGLANTISI
from binance.client import Client
client = Client(exchange_public_key,exchange_secret_key, {"verify":False, "timeout":20})

##############TÜM DEĞERLERİ ÇEKME

#tickers = client.get_ticker()
#for ticker in tickers:
    #print(tickers)

##############TüM VERİLERDEN BTC'Yİ ALIP BELGE YAPMA


candles_btcusdt_15min = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)
candles_btcusdt_1hr = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
candles_linkusdt_15min = client.get_klines(symbol='LINKUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)
import csv
with open('BTCUSDT_15min.csv','w', newline='') as csvfile:
    candle_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for candlestick in candles_btcusdt_15min:
        candlestick[0] = candlestick[0] / 1000
        candle_writer.writerow(candlestick)

csvfile.close()
with open('BTCUSDT_1hr.csv','w', newline='') as csvfile:
    candle_writer = csv.writer(csvfile, delimiter= ',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for candlestick in candles_btcusdt_1hr:
        candlestick[0] = candlestick[0] / 1000
        candle_writer.writerow(candlestick)
csvfile.close()

with open('LINKUSDT_15min.csv','w', newline='') as csvfile:
    candle_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for candlestick in candles_linkusdt_15min:
        candlestick[0] = candlestick[0] / 1000
        candle_writer.writerow(candlestick)
csvfile.close()






####### BELGEYİ NUMPY'LA İÇERİ ALMA #########
from numpy import genfromtxt

btcusdt_15min_data = genfromtxt('BTCUSDT_15min.csv', delimiter = ',')   ##Dosyayi içeri aldık.

high_price_btcusdt_15min = btcusdt_15min_data[:,2]
low_price_btcusdt_15min = btcusdt_15min_data[:,3]
close_price_btcusdt_15min = btcusdt_15min_data[:,4]           


btcusdt_1hr_data = genfromtxt('BTCUSDT_1hr.csv', delimiter = ',')   ##Dosyayi içeri aldık.

high_price_btcusdt_1hr = btcusdt_1hr_data[:,2]
low_price_btcusdt_1hr = btcusdt_1hr_data[:,3]
close_price_btcusdt_1hr = btcusdt_1hr_data[:,4]           

linkusdt_15min_data = genfromtxt('LINKUSDT_15min.csv', delimiter = ',')   ##Dosyayi içeri aldık.

high_price_linkusdt_15min = linkusdt_15min_data[:,2]
low_price_linkusdt_15min = linkusdt_15min_data[:,3]
close_price_linkusdt_15min = linkusdt_15min_data[:,4]   