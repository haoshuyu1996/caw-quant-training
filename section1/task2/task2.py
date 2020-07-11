from binance.client import Client
import pandas as pd
import datetime
import dateparser
import os

api_key = 'your api key'
api_secret = 'your api secret'

client = Client()
path = os.getcwd()


klines = client.get_historical_klines(
    "ETHBTC",
    Client.KLINE_INTERVAL_30MINUTE,
    "1 Dec, 2017",
    "1 Jan, 2018")
k = pd.DataFrame([k[:6] for k in klines], columns=[
                 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
k['Time'] = [dateparser.parse(str(d)) for d in k.Time]
k.sort_values(by='Time', ascending=False, inplace=True, ignore_index=True)
k.to_csv(os.path.join(path, 'candle data.csv'), index=False)

mktdepth = client.get_order_book(symbol="BNBBTC")
depth = pd.DataFrame([[b[0], b[1]]
                      for b in mktdepth['bids']], columns=['bids', 'bids_size'])
depth[['asks', 'asks_size']] = pd.DataFrame(
    [[a[0], a[1]] for a in mktdepth['asks']])
depth.to_csv(os.path.join(path, 'orderbook.csv'), index=False)

trade = client.get_recent_trades(symbol='BNBBTC')
trades = pd.DataFrame(trade)
trades = trades[['id', 'price', 'qty', 'time']]
trades['time'] = [dateparser.parse(str(d)) for d in trades.time]
trades.sort_values(by='time', ascending=False, inplace=True, ignore_index=True)
trades.to_csv(os.path.join(path, 'trade data.csv'), index=False)

client = Client(api_key=api_key, api_secret=api_secret)
order = client.create_test_order(
    symbol='ETHBTC',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=100)
order
