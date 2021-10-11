#release: python manage.py migrate
#web: gunicorn socialapp.wsgi
web: daphne socialapp.asgi:application --port 8001 --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2