from django.db import models


class HomePageSettings(models.Model):
    TIMEFRAME_CHOICES = [
        (5, '5m'),
        (15, '15m')
    ]

    timeframe = models.IntegerField(default=5, choices=TIMEFRAME_CHOICES)


class Coin(models.Model):
    name = models.CharField(max_length=255)


class CoinData(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=20, decimal_places=6)
    high = models.DecimalField(max_digits=20, decimal_places=6)
    low = models.DecimalField(max_digits=20, decimal_places=6)
    close = models.DecimalField(max_digits=20, decimal_places=6)
    volume = models.DecimalField(max_digits=20, decimal_places=4)
    time = models.DateTimeField(auto_now_add=False, auto_now=False)

    class Meta:
        unique_together = ('coin', 'time')


class CoinStatsRange(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    timeframe = models.IntegerField(default=5)  # Timeframe specified in minutes

    lower_latest_rsi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_latest_rsi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_adx = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_adx = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_ema = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_ema = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_roc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_roc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_beta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_beta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_sma_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_sma_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_super_trend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_super_trend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_slope_percent = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    upper_slope_percent = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lower_intercept = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    upper_intercept = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lower_r_squared = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    upper_r_squared = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lower_std_deviation = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    upper_std_deviation = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lower_closing_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    upper_closing_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('coin', 'timeframe',)


class CoinStatsCalculated(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    timeframe = models.IntegerField(default=5)  # Timeframe specified in minutes

    latest_rsi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    adx = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ema = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    beta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    super_trend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slope_percent = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    intercept = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    r_squared = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    std_deviation = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    closing_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('coin', 'timeframe',)


class CoinStatsHistorical(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    timeframe = models.IntegerField(default=5)  # Timeframe specified in minutes

    latest_rsi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    adx = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ema = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    beta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    super_trend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slope_percent = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    intercept = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    r_squared = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    std_deviation = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    closing_price = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)


class Trade(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=6)
    time = models.DateTimeField(auto_now=True)
