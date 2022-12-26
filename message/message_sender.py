import discord

from managers.file_manager import read_data
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


async def send_help(channel):
    prefix = read_data("data/config.json")["prefix"]
    help_text = f"**{prefix}list**:\n- sends a list of all serieses saved with the bot.\n**{prefix}add [name]**:\n- With add you can add a series to the bot.\n**{prefix}remove [name]**:\n- With remove you can remove the specified series from the bot.\n**{prefix}counter [name]**:\n- Counter sends the episode counter of the series you specified.\n**{prefix}rmcounter [name]**:\n- With rmcounter you can remove the specified episode counter form the channel chat.\n**{prefix}setep [name] [episode]**:\n- With setep you can set the episode of a series to the specified episode.\n**{prefix}setse [name] [season]**:\n- With setse you can set the season of a series to the specified season.\n**{prefix}adduser [series_name] @user**:\n- With adduser you can add users to your series so they can edit it aswell.\n**{prefix}rmuser [series_name] @user**:\n- With rmuser you can revoke a user the access to your series.\n- But be carefull, if you revoke all people the access to the series, the admin has to restore the permissons!"
    await send_message(channel, create_embeded("Welcome to the EpiCount help page, i hope this helps you.", help_text,
                                               discord.Color.from_rgb(255, 192, 203)), ["❌"])
