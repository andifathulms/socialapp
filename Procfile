#release: python manage.py migrate
#web: gunicorn socialapp.wsgi
web: daphne socialapp.asgi:application --port $PORT --bind 0.0.0.0:8000 -v2