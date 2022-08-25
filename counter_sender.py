import discord
import json
from message_sender import send_message
from chat_clearer import messageid


JSON_DATA_PATH = "/Users/lucdreibholz/GitHub/BotiBot/2wnty1ne-Discord-Bot/data/data.json"

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
    new_message = await send_message(channel=channel, title=data[key]["name"], description=f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]}', color=discord.Color.from_rgb(0,255,0), reactions=EMOJI_ARRAY)
    messageid[key] = new_message.id