import sys

import discord

from managers.data_management import has_link, has_filler
from managers.file_manager import read_data, write_data
from message.chat_clearer import messageid
from managers.filler_manager import check_if_filler
from message.message_sender import send_message, create_embeded

UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"
EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]


def create_counter_embeded(key):
    data = read_data()

    if has_filler(key):
        filler_array = check_if_filler(data[key]['episode'], key)
        is_filler, last_filler, epi_till_last = filler_array[0], filler_array[1], filler_array[2]
        filler_message = f'Filler Folge! Ende: {last_filler}, noch {epi_till_last} Folgen!'
        no_filler_message = 'Keine Filler Folge!'
        description = f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]} \n {filler_message if is_filler else no_filler_message}'
    else:
        description = f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]}'
    return create_embeded(data[key]["name"], description, discord.Color.from_rgb(0, 255, 0))


async def send_counter(channel, key):
    if not has_link(key):
        EMOJI_ARRAY.pop(3)
    # try:
    message = await send_message(channel, create_counter_embeded(key), EMOJI_ARRAY)
    messageid[key] = message.id
    return message
    # except Exception:
    #     print("Failed to send counter.")
