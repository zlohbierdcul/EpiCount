import discord


async def send_message(channel, title, description, color, reactions=None):
    if reactions is None:
        reactions = []
    embeded_message = discord.Embed(title=title, description=description, color=color)
    new_message = await channel.send(embed=embeded_message)
    for x in reactions:
        await new_message.add_reaction(x)

    return new_message
