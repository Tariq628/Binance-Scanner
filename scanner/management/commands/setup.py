from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from django.core.management.base import BaseCommand
from scanner.models import *
from scanner.utils import *
from scanner.tasks import get_historical_klines

import logging
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Listen to Binance WebSocket stream'
    queue = []
    lock = False

    def handle(self, *args, **options):
        # Create Coins

        coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'SOLUSDT',
                 'TRXUSDT', 'DOTUSDT', 'MATICUSDT', '1000SHIBUSDT', 'LTCUSDT',
                 'TONUSDT', 'WBTCUSDT', 'AVAXUSDT', 'LEOUSDT', 'BCHUSDT', 'LINKUSDT']

        for coin in coins:
            coin, created = Coin.objects.update_or_create(name=coin)

        # Create CoinStatsRange
        timeframes = [5, 15]
        for coin in coins:
            for timeframe in timeframes:
                coin_stats_range, created = CoinStatsRange.objects.update_or_create(
                    coin=Coin.objects.get(name=coin),
                    timeframe=timeframe
                )

        # Call celery task to fetch historical candles
        get_historical_klines.delay()
