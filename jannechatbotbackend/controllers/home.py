# -*- coding: utf-8 -*-
from bottle import Bottle, template
from bottle import post, get, put, delete, response, request

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatbot.chatbot import intro
from modules.chatbot.chatbot import store
home_app = Bottle()


@home_app.route('/')
def index():
    return intro()

@home_app.route('/post', 'POST')
def home():
    postdata = request.body.read()
    jsondata = json.loads(postdata)
    
    message = jsondata.get('message')
    return store(message)

@home_app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


