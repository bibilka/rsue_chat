release: python thebestchat/manage.py migrate
web: daphne -b 0.0.0.0 -p $PORT thebestchat.asgi:application