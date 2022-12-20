
from managers.file_manager import read_data, write_data


def add_series(name, auth_id):
    data = read_data()
    data[name.lower()] = ({'name': name, 'auth_id': [auth_id], 'episode': 1, 'season': 1})
    write_data(data)
