import re
import random
from bottle import response
from json import dumps
from common.dictionary.dictionary import reflections
from common.dictionary.dictionary import psychobabble
import datetime

optionMessage = [
    {"id": 1, "message": "Cari Property Di Bandung", "sender": "BOT"},
    {"id": 2, "message": "Saya sedang cari rumah", "sender": "BOT"},
    {"id": 3, "message": "i'm feeling lucky!", "sender": "BOT"}
]
introMessage = [
    {"id": 1, "message": "Janne the TeenBoT", "type": "message", "sender": "BOT"},
    {"id": 2, "message": "hi!! who r u??!", "type": "message", "sender": "BOT"},
    {
        "id": 3,
        "data": optionMessage,
        "type": "options",
        "message": "What do you want ?",
        "sender": "BOT"
    },
]


# reflect depends on reflections
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


# analyze is for get response from dictionary 
def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            resp = random.choice(responses)
            return resp.format(*[reflect(g) for g in match.groups()])


# intro is for introduce janne first message
def intro():
    response.content_type = 'application/json'
    data = {"data": introMessage, "status": 200, "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return dumps(data)


# store is for storing message
def store(message, type_message):
    while True:
        analyze_message = analyze(message)
        if type_message == "option":
            # get data from elasticsearch
            validate_message = get_data_from_es(analyze_message)
        else:
            validate_message = validate(analyze_message)

        data = {"data": validate_message, "status": 200, "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        response.content_type = 'application/json'
        response.status = 200
        return dumps(data)


# validate is for validation response
def validate(message):
    rv = {"id": 1, "message": message, "sender": "BOT"}

    options = [
        rv,
        {"id": 2, "data": optionMessage, "type": "options", "message": "What do you want ?", "sender": "BOT"}
    ]

    if message == "I dont understand what you said":
        return options
    else:
        return rv


# getDataFromElasticSearch retrive data from elasticsearch
def get_data_from_es(message):
    return message
