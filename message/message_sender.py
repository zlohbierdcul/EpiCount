import discord


async def send_message(channel, title, description, color, reactions=[]):
    global messageid

    embeded_message = discord.Embed(title=title, description=description, color=color)
    nice_message = await channel.send(embed=embeded_message)
    for x in reactions:
        await nice_message.add_reaction(x)

    return nice_message
