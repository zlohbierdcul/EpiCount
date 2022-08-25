import discord
import json
from message_sender import send_message


async def send_error(title, description, channel):
    await send_message(title=title, description=description, color=discord.Color.from_rgb(255, 0, 0))
