from ast import literal_eval
import asyncio

import discord
from discord.ui import Button, View

from managers.file_manager import read_data, write_data
from message.chat_clearer import countdown
from message.message_sender import send_message, create_embeded
from message.send_error import send_error


async def add(channel, name, auth_id, client):
    if name.lower() in read_data():
        await send_error("The series already exist!", "Please enter a valid series!", channel)
        return None
    link1 = "**website.com/some/path/{season}/{episode}**"
    link2 = "**website.com/some/path/{episode}**"
    embeded_link = create_embeded("Do you want to add a link?",
                                  f"A link has to have the following format:\n{discord.utils.escape_mentions(link1)} or\n{discord.utils.escape_mentions(link2)}.",
                                  discord.Color.from_rgb(0, 0, 255))
    embeded_filler = create_embeded("Do you want to add filler episodes?",
                                    f"The filler episodes have to be in the following format:\n **[15][18-19][22-30][99]**.\nNote: This is just an example, you can add as many fillers as you want.",
                                    discord.Color.from_rgb(0, 0, 255))

    async def button_yes_link_callback(interaction):
        await interaction.response.defer()
        yes_embeded = create_embeded("Please send the link.",
                                     f"A link has to have the following format:\n{discord.utils.escape_mentions(link1)} or\n{discord.utils.escape_mentions(link2)}.",
                                     discord.Color.from_rgb(0, 0, 255))
        await message_link.edit(embed=yes_embeded, view=None)
        response = await client.wait_for('message', check=lambda messages: messages.author == messages.author)
        await message_link.delete()
        # Return the user's input
        link = response.content
        if not link.startswith("http://") or not link.startswith("https://"):
            link = "https://" + link
        await add_filler(link)

    async def button_no_link_callback(interaction):
        await interaction.message.delete()
        await interaction.response.defer()
        link = ""
        await add_filler(link)

    button_yes_link = Button(label="Yes", style=discord.ButtonStyle.green)
    button_yes_link.callback = button_yes_link_callback
    button_no_link = Button(label="No", style=discord.ButtonStyle.red)
    button_no_link.callback = button_no_link_callback

    view_link = View()
    view_link.add_item(button_yes_link)
    view_link.add_item(button_no_link)
    message_link = await send_message(channel, embeded_link, view=view_link)

    async def add_filler(link):
        async def button_no_filler_callback(interaction):
            print(interaction.response)
            await interaction.message.delete()
            await interaction.response.defer()
            filler = []
            await add_series(channel, name, auth_id, filler, link)

        async def button_yes_filler_callback(interaction):
            await interaction.response.defer()
            yes_embeded_filler = create_embeded("Please send the filler episodes.",
                                            f"The filler episodes have to be in the following format:\n **[15][18-19][22-30][99]**.\nNote: This is just an example, you can add as many fillers as you want.",
                                            discord.Color.from_rgb(0, 0, 255))
            await message_filler.edit(embed=yes_embeded_filler, view=None)
            response = await client.wait_for('message', check=lambda messages: messages.author == messages.author)
            await message_filler.delete()
            # Return the user's input
            filler = literal_eval(response.content)
            await add_series(channel, name, auth_id, filler, link)
        button_yes_filler = Button(label="Yes", style=discord.ButtonStyle.green)
        button_yes_filler.callback = button_yes_filler_callback
        button_no_filler = Button(label="No", style=discord.ButtonStyle.red)
        button_no_filler.callback = button_no_filler_callback

        view_filler = View()
        view_filler.add_item(button_yes_filler)
        view_filler.add_item(button_no_filler)
        message_filler = await send_message(channel, embeded_filler, view=view_filler)


async def add_series(channel, name, auth_id, filler=None, link=None):
    global message
    data = read_data()
    try:
        data[name.lower()] = (
            {'name': name, 'auth_id': [auth_id], 'episode': 1, 'season': 1, 'filler': filler, 'link': link})
        message = await send_message(channel,
                           create_embeded(f'{name} has been added!',
                                          f'You can now use the following commands:\n!counter {name.lower()}\n!rmcounter {name.lower()}\n!setep {name.lower()}\n!setse {name.lower()}\n!rmseries {name.lower()}',
                                          discord.Color.from_rgb(0, 0, 255)))
    except Exception:
        print(Exception)
    write_data(data)
    if message:
        await asyncio.sleep(15)
        await message.delete()
