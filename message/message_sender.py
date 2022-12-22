import discord

from message.chat_clearer import messageid


def create_embeded(title, description, color):
    return discord.Embed(title=title, description=description, color=color)


async def send_message(channel, embeded, reactions=None, view=None):
    if reactions is None:
        reactions = []
    new_message = await channel.send(embed=embeded, view=view)
    for x in reactions:
        await new_message.add_reaction(x)
    return new_message
