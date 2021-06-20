import sys, getopt
import time
import pprint
import copy
import shared
import datetime
from botchart import BotChart
from botstrategy import BotStrategy
from botcandlestick import BotCandlestick
import ccxt
import argparse
argcollector = argparse.ArgumentParser()

argcollector.add_argument('-tframe', '--timeframe', type=str, default='1h',
                    help='time frame ex: 30s, 2m, 3h, 2d')
argcollector.add_argument('-cpair', '--currency_pair', type=str, default='BTC/USD',
                    help='currency pair to trade')
argcollector.add_argument('-sstamp', '--startstamp', type=str, default='',
                    help='start time stamp ex: 1494491969')
argcollector.add_argument('-estamp', '--endstamp', type=str, default='',
                    help='end time stamp ex: 1494491969')
argcollector.add_argument('-exch', '--exchange', type=str, default='bitmex',
                    help='exchange api ex: bitmex')
# argcollector.add_argument('-cpath', '--cpath', type=str, default='credential.txt',
#                           help='end time stamp ex: 1494491969')

# # todo read the api key and secret from a config file
# key_id = "tTcA6uzltuLz8PueS-3MnXSn"
# key_secret = "qkwWc0zzdh2ztoj_ip_Qq0haZicZqgvcRnOiuLaAGmgbGsws"




def main(argv):

    startTime = True
    endTime = False
    live = False
    movingAverageLength = 20


    # setting arguments

    timeframe = argv.timeframe
    # startTime = argv.startstamp
    endTime = argv.endstamp
    exchange = argv.exchange
    shared.exchange['name'] = exchange
    argv.currency_pair
    pair = argv.currency_pair
    shared.exchange['pair'] = pair
    shared.exchange['market'] = pair.split("/")[1]
    shared.exchange['coin'] = pair.split("/")[0]


    # startTime specified: we are in backtest mode
    if (startTime):

        chart = BotChart(timeframe, startTime, endTime)
        strategy = BotStrategy(backtest=True, live=live)
        strategy.showPortfolio()

        for candlestick in chart.getPoints():
            strategy.decide(candlestick)

        chart.drawChart(strategy.candlesticks, strategy.trades, strategy.movingAverages)

        strategy.showPortfolio()

    else:

        chart = BotChart(timeframe, False, False, False)

        strategy = BotStrategy(False, live)
        strategy.showPortfolio()

        candlestick = BotCandlestick()

        x = 0
        while True:
            try:
                currentPrice = chart.getCurrentPrice()
                candlestick.update(currentPrice)
                strategy.decide(candlestick)
                
            except ccxt.NetworkError as e:
                print(type(e).__name__, e.args, 'Exchange error (ignoring)')
            except ccxt.ExchangeError as e:
                print(type(e).__name__, e.args, 'Exchange error (ignoring)')
            except ccxt.DDoSProtection as e:
                print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
            except ccxt.RequestTimeout as e:
                print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
            except ccxt.ExchangeNotAvailable as e:
                print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
            except ccxt.AuthenticationError as e:
                print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')

            drawingCandles = copy.copy(strategy.candlesticks)
            if not candlestick.isClosed():
                drawingCandles.append(copy.copy(candlestick))
                drawingCandles[-1].close = candlestick.currentPrice
            chart.drawChart(drawingCandles, strategy.trades, strategy.movingAverages)

            if candlestick.isClosed():
                candlestick = BotCandlestick()

            x+=1
            time.sleep(int(1))

if __name__ == "__main__":

    args = argcollector.parse_args()

    # since_s= datetime.datetime(2021,4,19,0,0,0)
    # tnow = datetime.datetime.now().replace(second=0, microsecond=0)
    # tstop = datetime.datetime(2021,5,15,0,0,0)
    # int(datetimee.timestamp() )*1000

    args.startstamp = datetime.datetime(2019,1,1,0,0,0)
    args.endstamp = datetime.datetime.now().replace(second=0, microsecond=0)
    #datetime.datetime(2021,5,15,0,0,0)

    main( args )
    # read_credential("credential.txt")


