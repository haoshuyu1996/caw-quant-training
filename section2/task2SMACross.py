# Built-in libraries
import os
import datetime

# Third Party liabraries
import backtrader as bt
import pandas as pd
import matplotlib as plt

# Own Modules

# Environment params and global variables
datadir = './data'  # data path
logdir = './log'  # log path
reportdir = './report'  # report path
datafile = 'BTC_USDT_1h.csv'  # data file
logfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.csv'
figfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.png'
from_datetime = '2020-01-01 00:00:00'  # start time
to_datetime = '2020-04-01 00:00:00'  # end time
ticker = 'BTC'

# Strategy Class


class SMACross(bt.Strategy):

    params = (('pfast', 10), ('pslow', 20))

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        # Inital SMACross indicator
        sma1 = bt.ind.SMA(self.datas[0], period=self.p.pfast)
        sma2 = bt.ind.SMA(self.datas[0], period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'Buy {} shares of {} at {}'.format(
                        order.executed.size,
                        ticker,
                        order.executed.price))

            elif order.issell():
                self.log(
                    'Sell {} shares of {} at {}'.format(
                        order.executed.size,
                        ticker,
                        order.executed.price))
        else:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        # Setting the condition: whenever the SMA crossover is greater than
        # zero and not currently in a position, buy.
        if not self.position:
            if self.crossover > 0:
                self.buy()
        # Whenever the SMA crossover is less than zero and currently in a
        # position, close it.
        elif self.crossover < 0:
            self.close()


# Initiate cerebro instance
cerebro = bt.Cerebro()

# Feed data
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# Feed Strategy
cerebro.addstrategy(SMACross)

# Additional Settings
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# Add logger
cerebro.addwriter(
    bt.WriterFile,
    out=os.path.join(logdir, logfile),
    csv=True)

# Run
cerebro.run()

# Save report
plt.rcParams['figure.figsize'] = [13.8, 10]
fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
fig[0][0].savefig(
    os.path.join(reportdir, figfile),
    dpi=480)
