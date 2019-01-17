import re
import random
import datetime
from json import dumps
from bottle import response
from modules.smartsearch import SmartSearch
from common.dictionary.dictionary import reflections
from common.dictionary.dictionary import psychobabble

defaultResponse = "Mohon maaf, tolong masukan informasi yang lebih spesifik lagi"
optionMessage = [
    {"id": 1, "message": "Cari Property Di Bandung", "sender": "BOT"},
    {"id": 2, "message": "Saya sedang cari rumah", "sender": "BOT"},
    {"id": 3, "message": "i'm feeling lucky!", "sender": "BOT"}
]
introMessage = [
    {"id": 1, "message": "Nico the 99Bot", "type": "message", "sender": "BOT"},
    {"id": 2, "message": "Apa ada yang bisa saya bantu ?", "type": "message", "sender": "BOT"},
    {
        "id": 3,
        "data": optionMessage,
        "type": "options",
        "message": "Kami menyediakan beberapa opsi pertanyaan",
        "sender": "BOT"
    },
]
msg_residue = None
ss = SmartSearch()


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
            if analyze_message != defaultResponse:
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

    if message == defaultResponse:
        return options
    else:
        return rv


# get_data_from_es retrieve data from elastic search
def get_data_from_es(message):
    return ss.parser(message.lower())


# get_data_by_price retrieve data from elastic search
def get_data_by_price(message):
    return ss.parser(message.lower())
