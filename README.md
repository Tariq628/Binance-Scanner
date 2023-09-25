# BinanceScanner
A Binance Futures Scanner that calculates various TA attributes and triggers trades based on that.

Prerequisites:
1) Install redis (https://github.com/tporadowski/redis/releases)

Run the following commands in the given order.

celery -A BinanceScanner worker --loglevel=INFO -P gevent

python manage.py createsuperuser (Required only once)

python manage.py migrate

python manage.py runserver

python manage.py setup (Required only once)

python manage.py binance_ws_listener

