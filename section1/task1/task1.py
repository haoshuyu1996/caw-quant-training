import requests
import pandas as pd
from datetime import timezone
import datetime

def gethourdata(fsym, tsym, start_time, end_time, e):
    fromtime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
    totime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
    def getdata(time):
        url = 'https://min-api.cryptocompare.com/data/v2/histohour'
        params ={'fsym': fsym, 'tsym': tsym, 'toTs': time, 'e': e, 'limit':'2000'}
        results = requests.get(url, params=params)
        r = results.json()
        return r

    time = totime
    median = []
    while time > fromtime:
        data = getdata(time)
        median.append(pd.DataFrame(data['Data']['Data']))
        time = data['Data']['TimeFrom']
    histohour = pd.concat(median, axis=0)
    histohour = histohour[histohour['time'] >= fromtime]
    histohour['datetime'] = pd.to_datetime(histohour['time'], unit='s') 
    histohour[['datetime', 'close', 'high', 'low', 'open', 'volume', 'baseVolume']] = histohour[['datetime', 'close', 'high', 'low', 'open', 'volumefrom', 'volumeto']]
    histohour = histohour[['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']]
    histohour.sort_values(by = ['datetime'], inplace = True) 

    return histohour

df = gethourdata(fsym = 'BTC', tsym = 'USDT', start_time="2017-04-01 00:00:00", end_time="2020-04-01 00:00:00", e='binance')
df.to_csv(r'C:\Users\Louphero\Documents\GitHub\caw-quant-training\section1\task1\hourlydata.csv', index=False)
df