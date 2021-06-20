import ccxt
import shared


def BotApi():
    # switch to papermoney test
    ccxt.exchange = getattr(ccxt, shared.exchange['name'])({
        'apiKey': shared.api['key'],
        'secret': shared.api['secret']
        })

    if 'test' in ccxt.exchange.urls:
        ccxt.exchange.urls['api'] = ccxt.exchange.urls['test']  # ←----- switch the base URL to testnet

    return ccxt.exchange


