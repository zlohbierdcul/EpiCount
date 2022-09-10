import discord
import json
from message_sender import send_message
from chat_clearer import messageid
from filler_manager import check_if_filler


JSON_DATA_PATH = "data/data.json"

UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"



async def send_counter(key, channel):
    EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]

    with open(JSON_DATA_PATH, 'r') as x:
        data = json.load(x)

    if (key != 'onepiece'):
        EMOJI_ARRAY.pop(3)

    if (key == 'onepiece'):
        filler_array = check_if_filler(data[key]['episode'])
        is_filler = filler_array[0]
        last_filler = filler_array[1]
        epi_till_last = filler_array[2]
        filler_message = f'Filler Folge! Ende: {last_filler}, noch {epi_till_last} Folgen!'
        no_filler_message = 'Keine Filler Folge!'
    new_message = await send_message(channel=channel, title=data[key]["name"], description=f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]} \n {filler_message if is_filler else no_filler_message}', color=discord.Color.from_rgb(0,255,0), reactions=EMOJI_ARRAY)
    messageid[key] = new_message.id