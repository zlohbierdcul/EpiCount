import json

JSON_DATA_PATH = "../data/data.json"


def add_series(name, id):
    with open(JSON_DATA_PATH, "r") as x:
        data = json.load(x)

    print(data)
    data[name.lower()] = ({'name': name, 'auth_id': [id], 'episode': 1, 'season': 1})
    print(data)
    with open(JSON_DATA_PATH, 'w') as x:
        json.dump(data, x)

    print(data)