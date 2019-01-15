web: python manage.py runserver 0.0.0.0:5000
web: gunicorn gettingstarted.wsgi --log-file -
heroku ps:scale web=1