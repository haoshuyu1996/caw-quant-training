import requests
import pandas as pd
from datetime import timezone
import datetime


class get_CrptoCompare_data:

    def getfreqdata(
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
                url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym={}&tsym={}&toTs={}&limit=2000&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)
                results = requests.get(url)
                r = results.json()
                return r

            elif freq == 'hour':
                url = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym={}&toTs={}&limit=2000&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)
                results = requests.get(url)
                r = results.json()
                return r

            elif freq == 'minute':
                url = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym={}&tsym={}&toTs={}&limit=500&aggregate={}&e={}'.format(
                    fsym.upper(), tsym.upper(), time, aggregate, e)
                results = requests.get(url)
                r = results.json()
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
            histo.sort_values(by=['datetime'], inplace=True)

            return histo
        else:
            print(data['Message'])

    def mktcap_top(self, limit, tsym):
        url = 'https://min-api.cryptocompare.com/data/top/mktcapfull'
        params = {'limit': limit, 'tsym': tsym}
        results = requests.get(url, params=params)
        r = results.json()
        mktcaplist = []
        mktcap = []
        for i in range(limit):
            mktcaplist.append(r['Data'][i]['CoinInfo']['Name'])
            mktcap.append(r['Data'][i]['DISPLAY']['USD']['MKTCAP'])
        return pd.DataFrame({'top_list': mktcaplist, 'mktcap': mktcap})


df = get_CrptoCompare_data()
df.getfreqdata(
    fsym='BTC',
    tsym='USDT',
    start_time="2020-07-02 00:00:00",
    end_time="2020-07-03 00:00:00",
    e='binance',
    freq='minute',
    aggregate=2)
