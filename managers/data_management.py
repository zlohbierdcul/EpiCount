import json

from message.chat_clearer import messageid
from message.counter_remover import remove_counter

JSON_DATA_PATH = "../data/data.json"


async def remove_entry(key, channel):
    def should_be_removed(m):
        should_be_removed = False
        if m.id == messageid[key]:
            should_be_removed = True
        return should_be_removed

    await remove_counter(key, channel)

    with open(JSON_DATA_PATH, 'r') as x:
        data = json.load(x)
    print(key)
    if key in data:
        await channel.purge(check=should_be_removed)
        del data[key]
        print(f'{key} removed')
    else:
        print(f"{key} was not found")
    with open(JSON_DATA_PATH, 'w') as x:
        json.dump(data, x)