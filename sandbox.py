#
#
#
import time
import numpy as np
from datetime import datetime
# import schedule
import pandas as pd
# pd.set_option('option.')
import ccxt

import os
os.system('w32tm /resync')


key_id = "eBvXI0zzO7pgq6g1-le66L0r"
key_secret = "tFyj6ckkf_zbkdjArg7s3rt3hnd_lBuYJqb7ArA1eH2DeiRi"



def execute_order(order=None, exchange = None, params=None):

    # calculating the fee

    # if there is a buy order
    if order['action'] == 'buy':
        calex = exchange.calculateFee(order['symbol'], order['type'], order['action'], order['amount'], order['price'], takerOrMaker='taker', params={})

    if exchange.has['createMarketOrder']:
        pass

    order = exchange.create_order(order['symbol'], order['type'], side, order['amount'], order['price'], params)

    # cancel with order id
    exchange.cancel_order(  order['id'] )

    # if exchange.has['fetchOrders']:
    #     order = exchange.fetch_order(oid)
    # Python
    # add a custom order flag
    # exchange.create_market_buy_order( sam_symb, 1, {'trading_agreement': 'agree'})
    # exchange.create_limit_buy_order(symbol, amount, price, params])
    # exchange.create_limit_sell_order(symbol, amount, price, params])
    # exchange.createOrder(symbol, type, side, amount, price, {
    #    'clientOrderId': 'Hello',
    # })


    return True


def get_orders_report(arg):
    if exchange.has['fetchMyTrades']:
        myorders = exchange.fetch_my_trades(symbol=None, since=None, limit=None, params={})

    if exchange.has['fetchOpenOrders']:
        openords = exchange.fetchOpenOrders(symbol=sam_symb )

    if exchange.has['fetchClosedOrders']:
        exchange.fetchClosedOrders(symbol=sam_symb )




if __name__ == '__main__':

    exchange = ccxt.bitmex({
        'apiKey': key_id,
        'secret': key_secret,
    })

    # switch to papermoney test

    if 'test' in exchange.urls:
        exchange.urls['api'] = exchange.urls['test']  # ←----- switch the base URL to testnet
    print(exchange.fetch_balance())

    # get symbol list in the market
    markets = exchange.load_markets()

    sam_symb = 'ETH/USD'

    # get data and setting orders

    etheur2 = exchange.market(sam_symb)

    limit = 100

    ticker  = exchange.fetch_ticker( sam_symb )
    orderbook = exchange.fetch_order_book( sam_symb )
    trades = exchange.fetch_trades( sam_symb )


    # cleaning order cach
    # keep last hour of history in cache
    before = exchange.milliseconds() - 1 * 60 * 60 * 1000
    # purge all closed and canceled orders "older" or issued "before" that time
    # bitmex.purge_cached_orders(before)
    oid = exchange.market_id(sam_symb)

    symbol = sam_symb

    side = 'buy'
    amount = 1  # your amount
    price = ticker['bid']  # your price
    # overrides
    stopPrice = ticker['low']

    params = {}

    orderdict = { 'action':'buy', # buy, sell, cancel
                  'type': 'limit',  # or 'market', other types aren't unified yet, buy with limit price o by market price
                  'symbol': symbol,
                  'price': price, # price to buy (or sell)
                  'stopPrice': stopPrice, # (stop the order)
                  'amount' : 1,
                  "id": None
                  }

    res = execute_order(order=orderdict, exchange=exchange, params=None)

    if res:
        print(' the order is successful')
    else:
        print(' the order is unsuccessful')

    arg={}

    get_orders_report(arg)
    # get order report



    # watch_my_trades(symbol=None, since=None, limit=None, params={})

    # try to call a unified method
    """
    try:
        response = await exchange.fetch_order_book('ETH/BTC')
        print(response)
    except ccxt.NetworkError as e:
        print(exchange.id, 'fetch_order_book failed due to a network error:', str(e))
    # retry or whatever
    # ...
    except ccxt.ExchangeError as e:
        print(exchange.id, 'fetch_order_book failed due to exchange error:', str(e))
    # retry or whatever
    # ...
    except Exception as e:
        print(exchange.id, 'fetch_order_book failed with:', str(e))
        
    """


    # if exchange.has['fetchTransactions']:
    #     transactions = exchange.fetch_transactions(code, since, limit, params)
    # else:
    #     raise Exception(exchange.id + ' does not have the fetch_transactions method')

    """
    if exchange.has['fetchDeposits']:
        deposits = exchange.fetch_deposits(code, since, limit, params)
    else:
        raise Exception(exchange.id + ' does not have the fetch_deposits method')

    if exchange.has['fetchWithdrawals']:
        withdrawals = exchange.fetch_withdrawals(code, since, limit, params)
    else:
        raise Exception(exchange.id + ' does not have the fetch_withdrawals method')

    
    
    #
    bars = bitmex.fetch_ohlcv(sam_symb, timeframe='1d', limit=limit)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'] )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    order_book = ccxt.cex().fetch_order_book('BTC/USD', limit)

    # Python
    orderbook = bitmex.fetch_order_book(bitmex.symbols[0])
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    print(bitmex.id, 'market price', {'bid': bid, 'ask': ask, 'spread': spread})



    if bitmex.has['fetchOHLCV']:
        for symbol in bitmex.markets:
            time.sleep(bitmex.rateLimit / 1000)  # time.sleep wants seconds
    print(symbol, bitmex.fetch_ohlcv(symbol, '1d'))


    # bitmex = ccxt.coinbasepro()
    # print(bitmex.requiredCredentials)  # prints required credentials
    # bitmex.checkRequiredCredentials()

    # Python
    # params = {
    # 'foo': 'bar', # exchange-specific overrides in unified queries
    # 'Hello': 'World!', # see their docs for more details on parameter names
    # }
    # overrides go in the last argument to the unified call ↓ HERE
    result = bitmex.fetch_order_book( symbol )

    # Python
    # if bitmex.has['fetchOrders']:
    #     cursor = 0  # exchange-specific type and value
    #     all_orders = []
    #     while True:
    #         symbol = None  # change for your symbol
    #         since = None
    #         limit = 20  # change for your limit
    #         params = {
    #             'cursor': cursor,  # exchange-specific non-unified parameter name
    #                 }
    #         orders = await bitmex.fetch_orders(symbol, since, limit, params)
    #         if len(orders):
    #             # not thread-safu and exchange-specific !
    #             cursor = bitmex.last_response_headers['CB-AFTER']
    #             all_orders += orders
    #         else:
    #             break

    """
