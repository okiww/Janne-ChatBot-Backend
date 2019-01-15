# -*- coding: utf-8 -*-
from bottle import Bottle, template
from bottle import post, get, put, delete, response, request

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatbot.chatbot import intro
from modules.chatbot.chatbot import store
home_app = Bottle()


@home_app.route('/')
def index():
    return intro()

@home_app.route('/store')
def index():
    return store()

@home_app.route('/post', 'POST')
def home():
    postdata = request.body.read()
    print postdata #this goes to log file only, not to client
    name = postdata.name
    surname = request.forms.get("surname")
    return "Hi {name} {surname}".format(name=name, surname=surname)

@home_app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


