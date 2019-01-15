import re
import random
from bottle import response
from json import dumps
from common.dictionary.dictionary import reflections
from common.dictionary.dictionary import psychobabble

optionMessage = [
  {"id": 1, "message": "Cari Property Di Bandung"},
  {"id": 2, "message": "Saya sedang cari rumah"},
  {"id": 3, "message": "i'm feeling lucky!"}
]
introMessage = [
  { "id": 1, "message": "Janne the TeenBoT", "type": "message" }, 
  { "id": 2, "message": "hi!! who r u??!", "type": "message"},
  { 
    "id": 3, 
    "data": optionMessage,
    "type": "options"
  },
]

def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)
 
 
def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])
 
 
def main():
    print "Hello. How are you feeling today?"
    while True:
        statement = raw_input("> ")
        print "Hello. How are you feeling today?"
        print analyze(statement)
 
        if statement == "quit":
            break

def intro():
    response.content_type = 'application/json'
    return dumps(introMessage)

def store(message):
    while True:
      analyzeMessage = analyze(message)
      validateMessage = validate(analyzeMessage)
      
      response.content_type = 'application/json' 
      return dumps(validateMessage)

def validate(message):
  rv = { "id": 1, "message": message }
  options = [
    rv,
    {"id": 2, "data": optionMessage, "type": "options"}
  ]

  if message == "I dont understand what you said":
    return options
  else:
    return rv
