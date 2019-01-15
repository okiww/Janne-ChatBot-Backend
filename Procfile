web: python manage.py runserver 0.0.0.0:5000
web: gunicorn jannechatbot.wsgi --log-file -
heroku ps:scale web=2 worker=4