from ast import literal_eval
import asyncio

import discord
from discord.ui import Button, View

from managers.file_manager import read_data, write_data
from message.chat_clearer import countdown
from message.message_sender import send_message, create_embeded
from message.send_error import send_error


global handled_reactions
handled_reactions = set()


async def add(channel, name, auth_id, client):
    if name.lower() in read_data("data/data.json"):
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
        input_check = True
        while input_check:
            response = await client.wait_for('message', check=lambda messages: messages.author == messages.author)
            # Return the user's input
            link = response.content
            print(link)
            if not link.startswith("http://") and not link.startswith("https://"):
                link = "https://" + link
            new_link = "**<" + link + ">**"
            # escaped_link = discord.utils.escape_mentions(new_link)
            msg = await send_message(channel, create_embeded("Please confirm your input!",
                                                                          f"Do you want to add\n{new_link} to {name}?\n *Note: \nDue to the link having to be send as a hyperlink **{{** and **}}** are send as **%7B** and **%7D***",
                                                                          discord.Color.from_rgb(0, 255, 255)), ["✅", "❌"])
            handled_reactions.add(msg.id)
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: str(reaction.emoji) in ["✅", "❌"])
            print(reaction.emoji)
            if reaction.emoji == "❌":
                print("L")
                handled_reactions.remove(msg.id)
                await msg.delete()
            elif reaction.emoji == "✅":
                print("X")
                input_check = False
                handled_reactions.remove(msg.id)
                await msg.delete()
        await message_link.delete()
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
                                                f"The filler episodes have to be in the following format:\n **[15],[18,19],[22,30],[99]**.\nNote: This is just an example, you can add as many fillers as you want.",
                                                discord.Color.from_rgb(0, 0, 255))
            await message_filler.edit(embed=yes_embeded_filler, view=None)
            input_check = True
            while input_check:
                response = await client.wait_for('message', check=lambda messages: messages.author == messages.author)
                # Return the user's input
                try:
                    filler = literal_eval(response.content)
                    msg_filler = str(filler)[1:-1]
                except ValueError:
                    error = await send_error("Your input is not in the right format!", "Please try again!", channel)
                    await asyncio.sleep(4)
                    await error.delete()
                    continue
                confirmation_msg = await send_message(channel, create_embeded("Please confirm your input!",
                                                                              f"Do you want to add the filler\n**{msg_filler}** to {name}?",
                                                                              discord.Color.from_rgb(0, 255, 255)),
                                                      ["✅", "❌"])
                handled_reactions.add(confirmation_msg.id)
                reaction, user = await client.wait_for('reaction_add',
                                                       check=lambda reaction, user: str(reaction.emoji) in ["✅", "❌"])
                print(reaction.emoji)
                if reaction.emoji == "❌":
                    print("L")
                    handled_reactions.remove(confirmation_msg.id)
                    await confirmation_msg.delete()
                elif reaction.emoji == "✅":
                    print("X")
                    input_check = False
                    handled_reactions.remove(confirmation_msg.id)
                    await confirmation_msg.delete()
            await message_filler.delete()
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
    data = read_data('data/data.json')
    try:
        data[name.lower()] = (
            {'name': name, 'auth_id': [auth_id], 'episode': 1, 'season': 1, 'filler': filler, 'link': link})
        config = read_data("data/config.json")
        prefix = config["prefix"]
        message = await send_message(channel,
                                     create_embeded(f'{name} has been added!',
                                                    f'You can now use the following commands:\n{prefix}counter {name.lower()}\n{prefix}rmcounter {name.lower()}\n{prefix}setep {name.lower()}\n{prefix}setse {name.lower()}\n{prefix}rmseries {name.lower()}\n{prefix}adduser {name.lower()}\n{prefix}rmuser {name.lower()}',
                                                    discord.Color.from_rgb(0, 0, 255)))
    except Exception:
        print(Exception)
    write_data(data, 'data/data.json')
    if message:
        await asyncio.sleep(15)
        await message.delete()
