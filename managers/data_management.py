from managers.file_manager import read_data, write_data
from message.chat_clearer import messageid
from message.counter_remover import remove_counter


def has_filler(key):
    data = read_data()
    if 'filler' in data[key]:
        # TODO implement method
        pass


def has_link(key):
    data = read_data()
    if 'link' in data[key]:
        # TODO implement method
        pass


async def remove_entry(key, channel):
    data = read_data()

    def should_be_removed(m):
        removed = False
        if m.id == messageid[key]:
            removed = True
        return removed

    await remove_counter(key, channel)

    if key in data:
        await channel.purge(check=should_be_removed)
        del data[key]
        print(f'{key} removed')
    else:
        print(f"{key} was not found")

    write_data(data)
