import asyncio

import discord

from managers.file_manager import read_data, write_data
from message.chat_clearer import messageid, countdown
from message.counter_remover import remove_counter
from message.message_sender import send_message, create_embeded


def has_filler(key):
    data = read_data()
    return len(data[key]['filler']) > 1


def has_link(key):
    data = read_data()
    if data[key]['link'] is None:
        return False
    else:
        return True


async def remove_entry(key, channel):
    global message
    data = read_data()

    # def should_be_removed(m):
    #     removed = False
    #     if m.id == messageid[key]:
    #         removed = True
    #     return removed

    await remove_counter(key, channel)

    if key in data:
        # await channel.purge(check=should_be_removed)
        message = await send_message(channel, create_embeded("Series sucessfully removed!", f'{data[key]["name"]} is now no longer available.', discord.Color.from_rgb(0, 255, 0)))
        del data[key]
        print(f'{key} removed')
    else:
        print(f"{key} was not found")
    write_data(data)
    if message:
        await asyncio.sleep(5)
        await message.delete()
