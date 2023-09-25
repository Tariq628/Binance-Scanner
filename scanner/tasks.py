from celery import Celery
from celery.app import shared_task

from .models import Coin, CoinData
from .utils import *
import logging

from binance.client import Client


logger = logging.getLogger(__name__)


@shared_task
def get_historical_klines():
    client = Client('UMLne9tvM0WDHOMaUFTspKjqvYP0PHTkZxpyNFW4jdflIlZ76mm8ASK9VrHqG9Tk',
                    'YxSNGmO66BFCCDVovRG4pjkeyUtUQROG30948AbiJX8oikojbdFde3zh6V5LRJBo')

    symbols = Coin.objects.values_list('name', flat=True)
    for symbol in symbols:
        logger.info(f'Fetching for: {symbol}')
        try:
            coin_data = CoinData.objects.filter(coin=Coin.objects.get(name=symbol))
            if coin_data:
                coin_data = coin_data.order_by('-time')
                start_time = coin_data.first().time.strftime("%d %b %Y %H:%M:%S")
            else:
                start_time = '10 days ago UTC'
            klines = client.futures_historical_klines(symbol, '5m', start_time)
        except Exception as e:
            logger.info(
                f'Error fetching for {symbol}: {e}'
            )
            logger.error(e)
            continue

        for kline in klines:
            o = float(kline[1])
            h = float(kline[2])
            l = float(kline[3])
            c = float(kline[4])
            v = float(kline[5])

            timestamp = convert_timestamp_to_utc(kline[0]/1000)

            try:
                coin_data, created = CoinData.objects.update_or_create(
                    coin=Coin.objects.get(name=symbol),
                    time=timestamp,
                    defaults={
                        'open': o,
                        'high': h,
                        'low': l,
                        'close': c,
                        'volume': v
                    }
                )
            except Exception as e:
                logger.error(e)
                continue
