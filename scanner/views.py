from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Coin, CoinStatsRange, Trade


@login_required
def index(request):
    if request.GET.get('timeframe') is None:
        return redirect('/?timeframe=5')
    timeframe = request.GET.get('timeframe')
    coin_stats = CoinStatsRange.objects.filter(timeframe=timeframe).order_by('coin__name')
    context = {'coin_stats': coin_stats}
    return render(request, 'scanner/index.html', context)


@login_required
def trade_view(request):
    try:
        trade = Trade.objects.latest('time')
    except Exception as e:
        print(e)
        return JsonResponse({'trade': 'No trade found.'})

    return JsonResponse({
        'trade': f'buy {trade.coin.name} @ {float(trade.price)}'
    })


@csrf_exempt
def update_coin_stats(request):
    if request.method == 'POST':
        coin_name = request.POST.get('coin_name')
        timeframe = request.POST.get('timeframe')
        param_to_edit = request.POST.get('param_to_edit')
        value = request.POST.get('value')

        coin = get_object_or_404(Coin, name=coin_name)
        coin_stats_range, created = CoinStatsRange.objects.get_or_create(coin=coin, timeframe=timeframe)

        lower_value, upper_value = value.split(' - ')
        lower_value = None if lower_value is "" else float(lower_value)
        upper_value = None if upper_value is "" else float(upper_value)

        setattr(coin_stats_range, 'lower_' + param_to_edit, lower_value)
        setattr(coin_stats_range, 'upper_' + param_to_edit, upper_value)

        coin_stats_range.save()

        return HttpResponse('Coin stats updated successfully.')
    else:
        return HttpResponse('Invalid request method.')
