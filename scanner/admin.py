from django.contrib import admin
from .models import *


class CoinStatsCalculatedAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)


class CoinStatsHistoricalAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)


admin.site.register(Coin)
admin.site.register(CoinStatsRange)
admin.site.register(CoinStatsCalculated, CoinStatsCalculatedAdmin)
admin.site.register(CoinData)
admin.site.register(CoinStatsHistorical, CoinStatsHistoricalAdmin)
