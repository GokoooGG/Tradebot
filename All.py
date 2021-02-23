exchange_public_key = 'n7YeAc1LoHG28qbzAuSWS92m8ZX9uxtg4qo2fPpIehnMkWqmGPwbEove2pNVar4Q'
exchange_secret_key = 'WI1CWGX7EweNKpxHntj2UdaENzrzMuEm6CLFuoxHK6adyi3B4YZl6XvLnqpdOOsZ'


import psycopg2
import binance
import requests
import config
import csv

import backtrader as bt
from matplotlib.dates import warnings
        
cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname='LINKUSDT_15min.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes)
cerebro.adddata(data)

cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=.0025)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
#cerebro.addstrategy(rsi_taktigi)
#cerebro.addstrategy(TEMA_taktigi)
#cerebro.addstrategy(Stoch_taktigi)
#cerebro.addstrategy(Karma_taktik)
cerebro.addstrategy(karisik_kaset)
cerebro.run()

print('Final Portfolio Value: %.8f' % cerebro.broker.getvalue())

cerebro.plot()



####### INDIKATÖRLER #####
import talib
i = 0
n = 0
# 1 SAATLİK MACD
btcusdt_1hr_macd_hizli, btcusdt_1hr_macd_orta, btcusdt_1hr_macd_yavas = talib.MACD(close_price_btcusdt_1hr,fastperiod = 5,slowperiod = 14,signalperiod = 26)

## 15 DAKİKALIK MACD
btcusdt_15min_macd_hizli, btcusdt_15min_macd_orta, btcusdt_15min_macd_yavas = talib.MACD(close_price_btcusdt_15min,fastperiod = 5,slowperiod = 14,signalperiod = 26)

## 15 DAKİKALIK SRSI
fastk, fastd = talib.STOCHRSI(close_price_btcusdt_15min, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

## 15 DAKİKALIK RSI
rsi = talib.RSI(close_price_btcusdt_15min,timeperiod=14)  

# HEDEFLER VE ÇIKIŞ
atrdeger= talib.ATR(high_price_btcusdt_1hr,low_price_btcusdt_1hr,close_price_btcusdt_1hr, timeperiod= 48)

# 1 SAAT MACD TANIMLARI
son_btcusdt_1hr_macd_hizli = btcusdt_1hr_macd_hizli[-1]
son_btcusdt_1hr_macd_orta = btcusdt_1hr_macd_orta[-1]
son_btcusdt_1hr_macd_yavas = btcusdt_1hr_macd_yavas[-1]
# 15 DAKİKALIK MACD TANIMLARI
son_btcusdt_15min_macd_hizli = btcusdt_15min_macd_hizli[-1]
son_btcusdt_15min_macd_orta = btcusdt_15min_macd_orta[-1]
son_btcusdt_15min_macd_yavas = btcusdt_15min_macd_yavas[-1]
# 15 DAKİKALIK SRSI TANIMLARI
son_fastk = fastk[-1]
son_fastd = fastd[-1]
# 15 DAKİKALIK RSI TANIMLARI
son_rsi = rsi[-1]
asiri_alim = 70
asiri_satim = 30
# ATR TANIMI
son_atrdeger = atrdeger[-1]

#1 SAAT MACD 
if son_btcusdt_1hr_macd_yavas < close_price_btcusdt_1hr[-1]:
    print('Pozitif Trend', 'Long pozisyona uygun')
    i = i +1
else:
    print('Negatif Trend','Short pozisyona uygun')

# 15 dakikada indikatörlerin onayı (hepsi)
# MACD Onayı
if son_btcusdt_15min_macd_yavas < close_price_btcusdt_15min[-1]:
    if close_price_btcusdt_15min[-1] < son_btcusdt_15min_macd_orta:
        print('Pozisyona Giriş Onayı MACD')
        n = n+1
    else:
        print('Bekle MACD')
else:
    print('Pozisyon yok MACD')
# SRSI Onayı
if son_fastk >= son_fastd:
    print('Pozisyon Giriş Onayı SRSI')
    n = n+1
else:
    print('Bekle SRSI')
# RSI Onayı
if son_rsi >= asiri_alim:
    print('Pozisyon Yok RSI')
elif son_rsi <= asiri_satim:
    print('Pozisyona Giriş Onayı RSI')
    n= n+1
else:
    print('Bekle RSI')
# 5 dakikada elle onay
if i == 1:
    if n == 3:
        print('BTCUSDT Long Islem',
            'hedef 1:',close_price_btcusdt_15min[-1]+son_atrdeger*2,5,
              'Stop:', close_price_btcusdt_15min[-1]-son_atrdeger*1,5)
    else:
        print('BTCUSDT Pozisyona uygun değil')
else:
     print('BTCUSDT Pozisyona uygun değil')



##INDIKATOR 3 BOLLİNGERBANDS (SINIRLARIN DIŞINDA ALIM SATIM) ##4 SAATLIk
#upperband, middleband, lowerband = talib.BBANDS(close_price, timeperiod=32, nbdevup=3, nbdevdn=3, matype=0)
#print(upperband)



##RİSK FAKTÖRÜNÜ VERİYOR PORTFÖY ÇEŞİTLENDİRMEDE KULLANILACAK
#risk = talib.VAR(close_price,timeperiod=20,nbdev=1)
#print(risk)

##ATR DEĞERİ İÇİN 2-3 İÇİN KARI AL, -1.5 İÇİN POZİSYONDAN ÇIK
#atrdeger= talib.ATR(high_price,low_price,close_price, timeperiod= 50)
#print (atrdeger)

