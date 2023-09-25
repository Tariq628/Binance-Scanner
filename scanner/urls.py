from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_coin_stats', views.update_coin_stats, name='update_coin_stats'),
    path('trade', views.trade_view, name='trade_view'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    # Add more paths here
]
