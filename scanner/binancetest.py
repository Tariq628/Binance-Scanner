from binance.client import Client
from datetime import datetime

#
# client = Client('UMLne9tvM0WDHOMaUFTspKjqvYP0PHTkZxpyNFW4jdflIlZ76mm8ASK9VrHqG9Tk', 'YxSNGmO66BFCCDVovRG4pjkeyUtUQROG30948AbiJX8oikojbdFde3zh6V5LRJBo')
# klines = client.futures_historical_klines('BTCUSDT', '5m', '10 min ago UTC')
# print(datetime.utcfromtimestamp(klines[0][0]/1000))

import logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

def message_handler(_, message):
    print(message)


coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'USDCUSDT', 'ADAUSDT', 'DOGEUSDT', 'SOLUSDT', 'TRXUSDT', 'DOTUSDT', 'DAIUSDT', 'MATICUSDT', '1000SHIBUSDT', 'LTCUSDT', 'TONUSDT', 'WBTCUSDT', 'AVAXUSDT', 'LEOUSDT', 'BCHUSDT', 'LINKUSDT']
for c in coins:
    my_client = UMFuturesWebsocketClient(on_message=message_handler, is_combined=False)
    my_client.continuous_kline(c, 'perpetual', '5m', None, 'subscribe')

