import json

def load_json(questions):
    try:
        with open(questions,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("The data file is not found!")
        return []