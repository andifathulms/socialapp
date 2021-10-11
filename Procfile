#release: python manage.py migrate
#web: gunicorn socialapp.wsgi
web: daphne socialapp.asgi
worker: python manage.py runworker -v2