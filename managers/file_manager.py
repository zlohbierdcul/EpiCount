import json

JSON_DATA_PATH = "data/data.json"


def read_data(file):
    with open(file, "r") as data:
        return json.load(data)


def write_data(data, file):
    with open(file, "w") as x:
        json.dump(data, x)
