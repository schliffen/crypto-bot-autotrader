import numpy

from botcandlestick import BotCandlestick
from operator import attrgetter

class BotIndicators(object):
    def __init__(self):
         pass

    def averageTrueRange(self, tr, previousATRs=[], period = 5):
        previousATR = 0
        if len(previousATRs[-2:-1]) > 0:
            previousATR = previousATRs[-2:-1][0]
        atr = ((previousATR*(period-1))+tr)/period
        return atr

    def donchian_up(self, highs):
        return float(max(highs))

    def donchian_low(self, lows):
       return float(min(lows))

    def EMA(self, prices, period):
       x = numpy.asarray(prices)
       weights = None
       weights = numpy.exp(numpy.linspace(-1., 0., period))
       weights /= weights.sum()

       a = numpy.convolve(x, weights, mode='full')[:len(x)]
       a[:period] = a[period]
       return a

    def gmma(self, candlesticks, on='close', p1=3, p2=5, p3=8, p4=10, p5=12, p6=15):
        return [
            self.movingAverage(candlesticks, p1, on),
            self.movingAverage(candlesticks, p2, on),
            self.movingAverage(candlesticks, p3, on),
            self.movingAverage(candlesticks, p4, on),
            self.movingAverage(candlesticks, p5, on),
            self.movingAverage(candlesticks, p6, on)
            ]


    def heikinashi(self, currentCandle, previousHeikinashiCandle=False):
        if not previousHeikinashiCandle:
            o = (currentCandle.open+currentCandle.close)/2
        else:
            o = (previousHeikinashiCandle.open+previousHeikinashiCandle.close)/2

        c = (currentCandle.open+currentCandle.high+currentCandle.low+currentCandle.close)/4

        h = max((o, c, currentCandle.high))
        l = min((o, c, currentCandle.low))

        # return {'open': o, 'high': h, 'low': l, 'close': c, 'date': currentCandle.date}
        return BotCandlestick(14400,o,c,h,l,0, currentCandle.date)

    #ichimoku default periods are 9, 26, 26, here default values are adapted to crypto market
    def ichimoku(self, candlesticks, tenkanPeriod=10, kijunPeriod=30, senkouBPeriod=60, displacement=30):
        tenkan = kijun = senkouA = senkouB = chikou = False
        if len(candlesticks)>=tenkanPeriod:
            high = float(max(candlesticks[-tenkanPeriod:-1], key=attrgetter('high')).high)
            low = float(min(candlesticks[-tenkanPeriod:-1], key=attrgetter('low')).low)
            tenkan = (high+low)/2
        if len(candlesticks)>=kijunPeriod:
            high = float(max(candlesticks[-kijunPeriod:-1], key=attrgetter('high')).high)
            low = float(min(candlesticks[-kijunPeriod:-1], key=attrgetter('low')).low)
            kijun = (high+low)/2
        if tenkan and kijun:
            senkouA = (tenkan+kijun)/2
        if len(candlesticks)>=senkouBPeriod:
            high = float(max(candlesticks[-senkouBPeriod:-1], key=attrgetter('high')).high)
            low = float(min(candlesticks[-senkouBPeriod:-1], key=attrgetter('low')).low)
            senkouB = (high+low)/2
        if len(candlesticks)>=displacement:
            chikou = candlesticks[-1].close

        return {
            'tenkan': tenkan,
            'kijun':kijun,
            'senkouA': senkouA,
            'senkouB': senkouB,
            'chikou': chikou,
            'displacement': displacement
        }

    def MACD(self, prices, nslow=26, nfast=12):
        emaslow = self.EMA(prices, nslow)
        emafast = self.EMA(prices, nfast)
        return emaslow, emafast, emafast - emaslow

    def momentum (self, dataPoints, period=14):
        if (len(dataPoints) > period -1):
            return dataPoints[-1] * 100 / dataPoints[-period]

    def movingAverage(self, candlesticks, period, on='close'):
        if len(candlesticks) < period:
            period = len(candlesticks)
        dataPoints = [c.toDict()[on] for c in candlesticks[-period:]]
        return sum(dataPoints) / float(len(dataPoints))

    def RSI (self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(period - 1) + upval)/period
            down = (down*(period - 1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)
            if len(prices) > period:
                return rsi[-1]
            else:
                return 50 # output a neutral amount until enough prices in list to calculate RSI

    def trueRange(self, candles):
       atr1 = atr2 = atr3 = 0
       candles = candles[-2:]
       atr1 = abs(candles[-1].high - candles[-1].low)
       if len(candles) > 1:
           atr2 = abs(candles[-1].high - candles[-2].close)
           atr3 = abs(candles[-1].low - candles[-2].close)
       return max([atr1, atr2, atr3])

    def williamsFractal(self, candlesticks, period=2):
        bull = bear = False
        nbCandles = period*2+1
        if len(candlesticks)>nbCandles:
            candlesticks = candlesticks[-nbCandles:]
            #bullish fractal
            lows = [c.toDict()['low'] for c in candlesticks]
            if(lows.index(min(lows)) == period):
                bull = True
            #bearish fractal
            highs = [c.toDict()['high'] for c in candlesticks]
            if(highs.index(max(highs)) == period):
                bear = True
        return {
            'williamsFractalPeriod': period,
            'bullFractal': bull,
            'bearFractal': bear
        }
