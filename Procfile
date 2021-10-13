#release: python manage.py migrate
#web: gunicorn socialapp.wsgi
#web: daphne socialapp.asgi:application --port $PORT --bind 0.0.0.0 -v2
web: daphne -b 0.0.0.0 -p $PORT socialapp.asgi:application