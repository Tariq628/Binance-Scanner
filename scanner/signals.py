from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CoinData, CoinStatsCalculated
from .utils import *


@receiver(post_save, sender=CoinData)
def coin_data_post_save_handler(sender, instance, created, **kwargs):
    timeframes = [5, 15]
    for timeframe in timeframes:
        perform_new_calculations(instance.coin, timeframe=timeframe)


@receiver(post_save, sender=CoinStatsCalculated)
def coin_stats_calculated_post_save_handler(sender, instance, created, **kwargs):
    write_coin_stats_to_csv(instance)
    write_coin_stats_to_db(instance)

    if check_coin_stats_in_range(instance):
        generate_buy_signal(instance)
