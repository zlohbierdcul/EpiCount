import json

JSON_DATA_PATH = "data/data.json"


def read_data():
    with open(JSON_DATA_PATH, "r") as data:
        return json.load(data)


def write_data(data):
    with open(JSON_DATA_PATH, "w") as x:
        json.dump(data, x)
