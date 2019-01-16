# -*- coding: utf-8 -*-
from bottle import Bottle, template, route
from bottle import post, get, put, delete, response, request, run

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatbot.chatbot import intro
from modules.chatbot.chatbot import store
home_app = Bottle()


@route('/')
def index():
    return intro()

@route('/post', 'POST')
def home():
    postdata = request.body.read()
    jsondata = json.loads(postdata)
    
    message = jsondata.get('message')
    typeMessage = jsondata.get('type')
    return store(message, typeMessage)

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)

