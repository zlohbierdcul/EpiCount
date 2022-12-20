import json
import sys

import discord

from managers.data_management import has_link, has_filler
from managers.file_manager import read_data, write_data
from message.chat_clearer import messageid
from managers.filler_manager import check_if_filler
from message_sender import send_message

sys.path.append('../util')

# from file_manager import load_data
JSON_DATA_PATH = "../data/data.json"

UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"
EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]


async def send_counter(key, channel):
    data = read_data()

    if not has_link(key):
        EMOJI_ARRAY.pop(3)

    if has_filler(key):
        filler_array = check_if_filler(data[key]['episode'])
        is_filler = filler_array[0]
        last_filler = filler_array[1]
        epi_till_last = filler_array[2]
        filler_message = f'Filler Folge! Ende: {last_filler}, noch {epi_till_last} Folgen!'
        no_filler_message = 'Keine Filler Folge!'
        description = f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]} \n {filler_message if is_filler else no_filler_message}'
    else:
        description = f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]}'
    new_message = await send_message(channel=channel, title=data[key]["name"],
                                     description=description,
                                     color=discord.Color.from_rgb(0, 255, 0), reactions=EMOJI_ARRAY)
    messageid[key] = new_message.id
