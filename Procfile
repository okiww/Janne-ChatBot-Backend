web: python manage.py
web: gunicorn jannechatbot.wsgi --log-file -
heroku ps:scale web=2 worker=4