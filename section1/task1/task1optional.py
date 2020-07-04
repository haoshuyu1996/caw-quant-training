import requests
import pandas as pd
from datetime import timezone
import datetime
import difflib
import numpy as np
import os

pd.set_option('display.float_format', lambda x: '%.2f' % x)


class get_CryptoCompare_data:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://min-api.cryptocompare.com/data/'

    def get_coin_list(self):
        url = self.url + 'blockchain/list?api_key={}'.format(
            self.api_key)
        r = requests.get(url).json()

        if self.api_key:
            coin = pd.DataFrame.from_dict(r['Data'], orient='index')
            coin['data_available_from'] = [
                datetime.datetime.fromtimestamp(d) for d in coin.data_available_from]
            return coin
        else:
            raise Exception(r['Message'])

    def get_kline(
            self,
            fsym,
            tsym,
            start_time,
            end_time,
            e='binance',
            freq='daily',
            aggregate=1):

        fromtime = datetime.datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
        totime = datetime.datetime.strptime(
            end_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()

        def getdata(time):

            if freq == 'daily':
                url = self.url + 'v2/histoday?fsym={}&tsym={}&toTs={}&limit=2000&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)

            elif freq == 'hour':
                url = self.url + 'v2/histohour?fsym={}&tsym={}&toTs={}&limit=2000&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)

            elif freq == 'minute':
                url = self.url + 'v2/histominute?fsym={}&tsym={}&toTs={}&limit=500&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)
            else:
                raise Exception('Wrong frequency input')

            r = requests.get(url).json()
            return r

        time = totime
        median = []

        while time > fromtime:
            data = getdata(time)
            if data['Response'] == 'Error':
                break
            median.append(pd.DataFrame(data['Data']['Data']))
            time = data['Data']['TimeFrom']
        if median:

            histo = pd.concat(median, axis=0)
            histo = histo[histo['time'] >= fromtime]
            histo['datetime'] = pd.to_datetime(histo['time'], unit='s')
            histo[['datetime',
                   'close',
                   'high',
                   'low',
                   'open',
                   'volume',
                   'baseVolume']] = histo[['datetime',
                                           'close',
                                           'high',
                                           'low',
                                           'open',
                                           'volumefrom',
                                           'volumeto']]
            histo = histo[['close', 'high', 'low',
                           'open', 'volume', 'baseVolume', 'datetime']]
            histo.sort_values(by=['datetime'], inplace=True, ignore_index=True)

            return histo
        else:
            raise Exception(data['Message'])

    def get_top(self, by, limit, tsym='USD', fsym='BTC'):

        def get_url(url):
            results = requests.get(url)
            r = results.json()
            return r

        if by == 'mktcap' and tsym:
            url = self.url + \
                'top/mktcapfull?tsym={}&limit={}'.format(tsym, limit)
            r = get_url(url)
            mktcaplist = []
            mktcap = []
            for i in range(limit):
                mktcaplist.append(r['Data'][i]['CoinInfo']['Name'])
                mktcap.append(r['Data'][i]['DISPLAY']['USD']['MKTCAP'])
            return pd.DataFrame({'top_list': mktcaplist, 'mktcap': mktcap})

        elif by == 'volume' and tsym:
            url += self.url + 'top/volumes?tsym={}&limit={}'.format(
                tsym, limit)
            r = get_url(url)
            vol = pd.DataFrame(r['Data'])
            vol = vol[['SYMBOL', 'SUPPLY', 'NAME', 'VOLUME24HOURTO']]
            return vol

        elif by == 'pairs' and fsym:
            url += self.url + 'top/pairs?fsym={}&limit={}'.format(
                fsym, limit)
            r = get_url(url)
            vol = pd.DataFrame(r['Data'])
            vol = vol.drop('volume24hTo', axis=1)
            return vol

        else:
            raise Exception('wrong Sorting criteria')

    def get_order_book(
            self,
            fsym='BTC',
            tsym='USDT',
            limit=10,
            e='binance'):
        url = self.url + 'v2/ob/l2/snapshot?api_key={}&fsym={}&tsym={}&limit={}&e={}'.format(
            self.api_key, fsym, tsym, limit, e)
        r = requests.get(url).json()

        if self.api_key:
            order = pd.DataFrame(r['Data'])
            order = order[['FSYM', 'TSYM', 'BID', 'ASK']]
            orderbook = order[['FSYM', 'TSYM']]
            orderbook['BID'] = [b['P'] for b in order.BID]
            orderbook['BID_Q'] = [b['Q'] for b in order.BID]
            orderbook['ASK'] = [a['P'] for a in order.ASK]
            orderbook['ASK_Q'] = [a['Q'] for a in order.ASK]
            return orderbook

        else:
            raise Exception(r['Message'])


df = get_CryptoCompare_data(
    api_key='ec53d4894590ba366edfbaafe2a19d2856483a2de3c53726f871c0e671fc9b11')
df.get_coin_list()
df.get_top(by='mktcap', limit=10)
df.get_order_book(
    limit=20,
    e='binance')
kline = df.get_kline(
    fsym='BTC',
    tsym='USDT',
    start_time='2017-04-01 00:00:00',
    end_time='2020-04-01 00:00:00',
    e='binance',
    freq='hour',
    aggregate=1)

path = os.getcwd()
path = os.path.join(path, 'hourlydata.csv')
kline.to_csv(path, index=False)
