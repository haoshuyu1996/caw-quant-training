# Built-in libraries
import os
import datetime

# Third Party liabraries
import backtrader as bt
import pandas as pd
import matplotlib as plt
import numpy as np

# Own Modules

# Environment params and global variables
datadir = './data'  # data path
logdir = './log'  # log path
reportdir = './report'  # report path
datafile = 'BTC_USDT_1h.csv'  # data file
logfile = 'BTC_USDT_1h_SMACrossOpt_10_20_2020-01-01_2020-04-01.csv'
figfile = 'BTC_USDT_1h_SMACrossOpt_10_20_2020-01-01_2020-04-01.png'
optfile = 'BTC_USDT_1h_SMACrossBest_10_20_2020-01-01_2020-04-01.csv'
from_datetime = '2020-01-01 00:00:00'  # start time
to_datetime = '2020-04-01 00:00:00'  # end time
ticker = 'BTC'

# Strategy Class


class SMACross(bt.Strategy):

    params = (('pfast', 10), ('pslow', 20))

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        # Inital SMACross indicator
        sma1 = bt.ind.SMA(self.datas[0], period=self.p.pfast)
        sma2 = bt.ind.SMA(self.datas[0], period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        # I don't want to optimize the strategy when the fast slow pairs do not match
        # But it still generate an output but without any data, I wonder is there a way
        # that do not even optimize the strategy when pfast and pslow do not
        # match certain conditions
        if self.p.pslow >= self.p.pfast:
            if not self.position:
                if self.crossover > 0:
                    self.buy()

            elif self.crossover < 0:
                self.close()
        else:
            pass

    def stop(self):
        if self.p.pslow >= self.p.pfast + 5:
            self.log(
                '(SMACross Period fast %2d, slow %2d) Ending Value %.2f' %
                (self.params.pfast, self.params.pslow, self.broker.getvalue()))
        else:
            pass


# Initiate cerebro instance
cerebro = bt.Cerebro(optreturn=False)

# Optimize Strategy
strats = cerebro.optstrategy(SMACross, pfast=range(5, 21), pslow=range(10, 51))

# Feed data
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# Additional Settings
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# Feed Analyzer
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)

# Add logger
# cerebro.addwriter(
#	bt.WriterFile,
#	out=os.path.join(logdir, logfile),
#	csv=True)

# Run
runs = cerebro.run(maxcpus=1)

# Find the most profitable result within the periods range only according
# to different period pairs.
final_results = []
for run in runs:
    optvalue = run[0].broker.getvalue()
    print(optvalue)
    pf = run[0].params.pfast
    ps = run[0].params.pslow
    final_results.append([[pf, ps], optvalue])

by_value = sorted(final_results, key=lambda x: x[1], reverse=True)

print(
    'your most profitable optimization period is (fast %2d, slow %2d) with a Ending Value of %.2f' %
     (by_value[0][0][0], by_value[0][0][1], by_value[0][1]))

# But the problem is each strategy in runs contains only the last
# strategy's ending value

# Save report
#plt.rcParams['figure.figsize'] = [13.8, 10]
#fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
# fig[0][0].savefig(
#	os.path.join(reportdir, figfile),
#	dpi=480)

resultslist = []

for run in runs:
    for strategy in run:
        P = strategy.params
        RET = strategy.analyzers.returns.get_analysis()
        DD = strategy.analyzers.drawdown.get_analysis()
        TrAn = strategy.analyzers.tradeanalyzer.get_analysis()
        # I filter the fast slow pairs here
        if P.pslow >= (P.pfast + 5):
            pf = P.pfast
            ps = P.pslow
            # The bt.analyzers.Return gives you the return based only on the
            # assets you hold instead of the whole portfolio value
            ret = RET['rtot']
            maxd = DD.max.drawdown
            totalTrades = TrAn.total.total
            wintrades = TrAn.won.total
            losstrades = TrAn.lost.total
            winratio = wintrades / totalTrades
            averagewin = TrAn.won.pnl.total / wintrades
            averageloss = TrAn.lost.pnl.total / losstrades
            avgwlratio = averagewin / averageloss
            logestwinstreak = TrAn.streak.won['longest']
            logestlossstreak = TrAn.streak.lost['longest']
            resultslist.append(['SMACross',
                                pf,
                                ps,
                                ret,
                                maxd,
                                totalTrades,
                                wintrades,
                                losstrades,
                                winratio,
                                averagewin,
                                averageloss,
                                logestwinstreak,
                                logestlossstreak,
                                avgwlratio])

df = pd.DataFrame(
    resultslist,
    columns=[
        'Name',
        'sma_pfast',
        'sma_pslow',
        'Return',
        'MaxDrawDown',
        'TotalTrades#',
        'winTrades#',
        'LossTrades#',
        'WinRatio',
        'AverageWin$',
        'AverageLoss$',
        'LongestWinStreak',
        'LongestLossStreak',
        'AverageWinLossRatio'])

df['RankReturn'] = df['Return'].rank(ascending=False)
df['RankMaxDrawDown'] = df['MaxDrawDown'].rank(ascending=False)
df['RankWinRatio'] = df['WinRatio'].rank(ascending=False)
df['RankAverageWinLossRatio'] = df['AverageWinLossRatio'].rank(ascending=False)
df['Score'] = (df['RankReturn'] + df['RankMaxDrawDown'] +
               df['RankWinRatio'] + df['RankAverageWinLossRatio']) / 4
df = df.round(4)
df

print('The best Portfolio within the iteration period:')
print(df.loc[df['Score'] == np.min(df['Score'])])

df.to_csv(os.path.join(reportdir, optfile))
