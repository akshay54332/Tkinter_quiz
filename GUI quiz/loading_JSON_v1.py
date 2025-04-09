import json

def load_json(questions):
    with open(questions,'r') as file:
        return json.load(file)