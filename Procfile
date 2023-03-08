release: python backend/manage.py makemigrations --no-input
release: python backend/manage.py migrate --no-input

web: gunicorn backend.wsgi
web: python backend/manage.py runserver 0.0.0.0:$PORT
