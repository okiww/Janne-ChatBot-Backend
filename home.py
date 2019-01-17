# -*- coding: utf-8 -*-
import bottle
from bottle import Bottle, template, route
from bottle import post, get, put, delete, response, request, run

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatbot.chatbot import intro
from modules.chatbot.chatbot import store

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

home_app = Bottle()   

@route('/')
@enable_cors
def index():
    return intro()

@route('/post', 'POST')
@enable_cors
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

