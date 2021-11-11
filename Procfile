web: gunicorn thebestchat.thebestchat.wsgi:application --log-file - --log-level debug
python thebestchat.manage.py collectstatic --noinput
manage.py migrate