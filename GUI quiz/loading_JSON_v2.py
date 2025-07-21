import json
import os
import csv

def load_json(questions):
    try:
        with open(questions,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("The data file is not found!")
        return []
    

# for checking if the file exist...
def get_file_path(data_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir,data_file)

    return file_path

def is_file(data_file):
    file_path = get_file_path(data_file)
    file_exist = os.path.exists(file_path)
    return file_exist

def store(name, score):
    file_path = is_file('scoreBoard.csv')

    if file_path:
        with open('scoreBoard.csv','a', newline="") as file:
            fieldnames = ['first_name','score']
            csvwriter = csv.DictWriter(file, fieldnames=fieldnames)
            csvwriter.writerow({"first_name":name, "score": score})

    else:
        with open('scoreBoard.csv','a', newline="") as file:
            fieldnames = ['first_name','score']
            csvwriter = csv.DictWriter(file, fieldnames=fieldnames)
            csvwriter.writeheader()
            csvwriter.writerow({"first_name":name, "score": score})
