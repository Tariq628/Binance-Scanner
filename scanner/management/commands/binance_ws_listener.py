from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from django.core.management.base import BaseCommand
from scanner.models import Coin, CoinData
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
        # Handle incoming messages from Binance Socket
        def message_handler(_, message):
            msg = json.loads(message)
            if "ps" not in msg:
                if "result" and "id" in msg:
                    return
                logger.warning("Unexpected behavior in Binance Web Socket stream")
                logger.warning(msg)
                return

            data = {
                'open': round(float(msg['k']['o']), 6),
                'high': round(float(msg['k']['h']), 6),
                'low': round(float(msg['k']['l']), 6),
                'close': round(float(msg['k']['c']), 6),
                'volume':  round(float(msg['k']['v']), 2),
                'time': convert_timestamp_to_utc(msg['k']['t']/1000),
                'symbol': Coin.objects.get(name=msg['ps'])
            }

            print(f"{data['symbol'].name}: {data['close']}")

            self.queue.append(data)
            if self.lock is True:
                return

            self.lock = True
            while self.queue:
                try:
                    data = self.queue.pop(0)
                    coin_data, created = CoinData.objects.update_or_create(
                        coin=data['symbol'],
                        time=data['time'],
                        defaults={
                            'open': data['open'],
                            'high': data['high'],
                            'low': data['low'],
                            'close': data['close'],
                            'volume': data['volume']
                        }
                    )

                except Exception as e:
                    logger.error("Error saving coin data for symbol: " + data['symbol'].name)
                    logger.error(e)
                    print(data)

            self.lock = False

        # Fetch previous missing candles before fetching live candles
        get_historical_klines_task = get_historical_klines.delay()
        get_historical_klines_task.get()

        # Subscribe to stream for every coin
        for c_ in Coin.objects.values_list('name', flat=True):
            ws_client = UMFuturesWebsocketClient(on_message=message_handler)
            ws_client.continuous_kline(c_, 'perpetual', '5m', None, 'subscribe')

    def handle_sigint(self, signum, frame):
        print("\nWebSocket connection closed. Exiting gracefully.")
        exit(0)
