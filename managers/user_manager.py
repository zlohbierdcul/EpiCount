import asyncio

import discord

from managers.file_manager import read_data, write_data
from message.message_sender import send_message, create_embeded
from message.send_error import send_error


async def add_user(channel, key, users, user):
    data = read_data('data/data.json')
    if not check_auth(user, key):
        error_message = await send_error("You´re not authorized to do that!", "Fuck off now!", channel)
        await asyncio.sleep(2)
        await error_message.delete()
        return None
    user_names = []
    for user in users:
        if user.id not in data[key]["auth_id"]:
            data[key]["auth_id"].append(user.id)
            user_names.append(user.name)
    name_string = " ,".join(user_names)
    message = await send_message(channel, create_embeded(f"Users added to {data[key]['name']}",
                                                         f"{name_string} have been added sucessfully" if (
                                                                 len(user_names) > 1) else f"{name_string} has been added sucessfully",
                                                         discord.Color.from_rgb(0, 255, 0)))
    write_data(data, 'data/data.json')
    await asyncio.sleep(8)
    await message.delete()


async def remove_user(channel, key, users, user):
    data = read_data('data/data.json')
    user_names = []
    if not check_auth(user, key):
        message = await send_error("You´re not authorized to do that!", "Fuck off now!", channel)
        await asyncio.sleep(2)
        await message.delete()
        return None
    for user in users:
        if user.id in data[key]["auth_id"]:
            data[key]["auth_id"].remove(user.id)
            user_names.append(user.name)
    name_string = " ,".join(user_names)
    message = await send_message(channel, create_embeded(f"Users removed from {data[key]['name']}",
                                                         f"{name_string} have been removed sucessfully" if (
                                                                     len(user_names) > 1) else f"{name_string} has been removed sucessfully",
                                                         discord.Color.from_rgb(0, 255, 0)))
    write_data(data, 'data/data.json')
    await asyncio.sleep(8)
    await message.delete()


def check_auth(user_id, key):
    data = read_data('data/data.json')
    config = read_data('data/config.json')
    if user_id in data[key]['auth_id'] or user_id == config['admin']:
        return True
    else:
        return False
