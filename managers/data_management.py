import asyncio

import discord

from managers.file_manager import read_data, write_data
from managers.user_manager import check_auth
from message.counter_remover import remove_counter
from message.message_sender import send_message, create_embeded
from message.send_error import send_error


def has_filler(key):
    data = read_data('data/data.json')
    return len(data[key]['filler']) > 1


def has_link(key):
    data = read_data('data/data.json')
    if data[key]['link'] is None:
        return False
    else:
        return True


async def remove_entry(key, channel, user):
    global message
    data = read_data('data/data.json')
    if not check_auth(user, key):
        message = await send_error("You´re not authorized to do that!", "Fuck off now!", channel)
        await asyncio.sleep(2)
        await message.delete()
        return None
    await remove_counter(key, channel)

    if key in data:
        message = await send_message(channel, create_embeded("Series sucessfully removed!", f'{data[key]["name"]} is now no longer available.', discord.Color.from_rgb(0, 255, 0)))
        del data[key]
        print(f'{key} removed')
    else:
        print(f"{key} was not found")
    write_data(data, 'data/data.json')
    if message:
        await asyncio.sleep(5)
        await message.delete()


async def list_series(channel):
    data = read_data("data/data.json")
    names_string = '\n'.join(['- ' + value["name"] for key, value in data.items()])
    list_msg = await send_message(channel, create_embeded("The following serieses are available.", f"{names_string}",
                                               discord.Color.from_rgb(0, 255, 0)))
    await asyncio.sleep(15)
    await list_msg.delete()
