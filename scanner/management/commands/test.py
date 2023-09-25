from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from django.core.management.base import BaseCommand
from scanner.models import *
from scanner.utils import *

import logging
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Listen to Binance WebSocket stream'
    queue = []
    lock = False

    def handle(self, *args, **options):
        coin = Coin.objects.get(name='USDCUSDT')
        print(coin.id)
        perform_new_calculations(coin, timeframe=5)
