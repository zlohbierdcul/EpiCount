import discord

from message.message_sender import send_message, create_embeded


async def send_error(title, description, channel):
    return await send_message(channel, create_embeded(title, description, discord.Color.from_rgb(255, 0, 0)))
