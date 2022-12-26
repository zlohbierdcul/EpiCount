import asyncio
import os
import webbrowser

import discord
from dotenv import load_dotenv

from managers.config_manager import not_configured, configure_bot
from managers.file_manager import read_data, write_data
from managers.user_manager import add_user, remove_user, check_auth
from message import counter_sender
from message.counter_sender import create_counter_embeded
from message.send_error import send_error
from util import link_generator, series_adder
from message.chat_clearer import clear_chat, messageid, countdown
from message.counter_remover import remove_counter
from managers.data_management import remove_entry, list_series
from managers.filler_manager import check_if_filler
from message.message_sender import send_message, create_embeded, send_help
from util.link_generator import get_link
from util.series_adder import handled_reactions

load_dotenv()

# discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# ? Bot client configuration
intents = discord.Intents.all()
bot = discord.Client(intents=intents, )

ADMIN_USER_ID = [409486429392207873]

UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"

EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]


# ? Gets executed when the bot starts
@bot.event
async def on_ready():
    try:
        channel = bot.get_channel(read_data("data/config.json")["channel"])
        await clear_chat(channel)
    except Exception:
        print("channel not definded")
    guilds = bot.guilds
    print(f"\n{bot.user} is ready\nConnected to {len(guilds)} Server\n")


async def reload_message(key):
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    message_obj = await channel.fetch_message(messageid[key])
    await message_obj.edit(embed=create_counter_embeded(key))


def commands_to_lower(command_list):
    command_list_lower = []
    for x in range(len(command_list)):
        command_list_lower.append(command_list[x].lower())
    return command_list_lower


def format_time(minutes):
    hours_total = minutes // 60
    # Get additional minutes with modulus
    minutes_total = minutes % 60
    # Create time as a string
    time_string = "{} hours {} minutes".format(hours_total, minutes_total)
    return time_string


async def set_episode(key, num, user):
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    data = read_data('data/data.json')
    if not check_auth(user, key):
        error_msg = await send_error("You´re not authorized to do that!", "Fuck off now!", channel)
        await asyncio.sleep(2)
        await error_msg.delete()
        return None
    try:
        data[key]["episode"] = int(num)
    except Exception:
        err = await send_error("The series does not exist!", "Please enter a valid series!", channel)
        await asyncio.sleep(2)
        await err.delete()
    write_data(data, 'data/data.json')
    await reload_message(key)


async def set_season(key, num, user):
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    data = read_data('data/data.json')
    if not check_auth(user, key):
        error_msg = await send_error("You´re not authorized to do that!", "Fuck off now!", channel)
        await asyncio.sleep(2)
        await error_msg.delete()
        return None
    try:
        data[key]["season"] = int(num)
    except Exception:
        await send_error("The series does not exist!", "Please enter a valid series!", channel)
    write_data(data, 'data/data.json')
    await reload_message(key)


async def calculate_watchtime():
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    data = read_data('data/data.json')
    watchtime = data["onepiece"]["episode"] * 20
    watchtime_hours = format_time(watchtime)
    embeded_message = discord.Embed(title="Watchtime",
                                    description=f'{watchtime} min or {watchtime_hours}\nhave been watched!',
                                    color=discord.Color.from_rgb(0, 0, 255))
    message = await channel.send(embed=embeded_message)
    await asyncio.sleep(10)
    await message.delete()


def get_key(message_id):
    for x in messageid:
        if message_id == messageid[x]:
            return x


async def handle_reaction(payload):
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    data = read_data('data/data.json')
    key = get_key(payload.message_id)

    if payload.emoji.name == UP_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] + 1
    if payload.emoji.name == DOWN_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] - 1
    if payload.emoji.name == PLUS_EMOJI:
        data[key]["season"] = data[key]["season"] + 1

    write_data(data, 'data/data.json')
    await reload_message(key)

    if payload.emoji.name == LINK_EMOJI:
        embeded = create_embeded(f'Link to {data[key]["name"]}',
                                 "",
                                 discord.Color.from_rgb(0, 0, 255))
        embeded.url = get_link(key)
        message = await send_message(channel,
                                     embeded)
        await asyncio.sleep(10)
        await message.delete()


@bot.event
async def on_raw_reaction_add(payload):
    config = read_data("data/config.json")
    channel = bot.get_channel(config["channel"])
    if payload.message_id in handled_reactions:
        return
    if not payload.user_id == bot.user.id:
        try:
            message_obj = await channel.fetch_message(payload.message_id)
            user_obj = bot.get_user(payload.user_id)
            await message_obj.remove_reaction(payload.emoji.name, user_obj)
            if payload.emoji.name == "❌":
                print("X main")
                await message_obj.delete()
                return None
            admin_or_link = check_auth(payload.user_id, get_key(message_obj.id)) or (payload.emoji.name == LINK_EMOJI)
            if (payload.channel_id == channel.id) and admin_or_link and not (payload.user_id == bot.user.id):
                await handle_reaction(payload)
            elif not payload.user_id == bot.user.id:
                awaited_channel = bot.get_channel(payload.channel_id)
                error_message = await send_error("You´re not authorized to do that!", "Fuck off now!", awaited_channel)
                await asyncio.sleep(2)
                await error_message.delete()
        except Exception:
            print("shit")


configuring = False


@bot.event
async def on_message(message):
    global configuring
    messager_id = message.author.id
    config = read_data("data/config.json")
    if messager_id == bot.user.id or message.content is None:
        if not configuring:
            if message.channel.id != config["channel"]:
                return None
        return None

    if not_configured(config) and not configuring:
        print("configuring")
        configuring = True
        config["channel"] = message.channel.id
        write_data(config, "data/config.json")
        config_msg = await send_message(message.channel, create_embeded("Please send the prefix you want to use!",
                                                                        "Suggestions: **!**, **.** or **?**",
                                                                        discord.Color.from_rgb(0, 255, 255)))
        response = await bot.wait_for('message', check=lambda messages: messages.author == messages.author)
        await config_msg.delete()
        await message.delete()
        config["prefix"] = response.content
        bot.activity = discord.Game(name=f'prefix: {config["prefix"]}')
        config["admin"] = message.author.id
        write_data(config, "data/config.json")
        sucess_msg = await send_message(message.channel, create_embeded("Bot has been configured!",
                                                                        f"This bot is now available in this channel "
                                                                        f"using the prefix **{config['prefix']}**",
                                                                        discord.Color.from_rgb(0, 255, 255)))
        await asyncio.sleep(10)
        await sucess_msg.delete()
        return None

    await message.delete()
    command_message = message.content
    command_list = command_message.split()
    command = command_list.pop(0)
    command_args = command_list

    try:
        channel = bot.get_channel(config['channel'])
        prefix = config['prefix']
    except Exception:
        return None
    if command == f'{prefix}list':
        await list_series(channel)
    if command == f'{prefix}help':
        await send_help(channel)
    if command == f'{prefix}remove':
        await remove_entry(command_args[0].lower(), channel, message.author.id)
    if command == f'{prefix}counter':
        await counter_sender.send_counter(channel, command_args[0].lower())
    if command == f'{prefix}rmcounter':
        await remove_counter(command_args[0].lower(), channel)
    if command == f'{prefix}add':
        await series_adder.add(channel, command_args[0], messager_id, bot)
    if command == f'{prefix}setep':
        await set_episode(command_args[0].lower(), command_args[1], message.author.id)
    if command == f'{prefix}setse':
        await set_season(command_args[0].lower(), command_args[1], message.author.id)
    if command == f'{prefix}adduser':
        await add_user(channel, command_args[0].lower(), message.mentions, message.author.id)
    if command == f'{prefix}rmuser':
        await remove_user(channel, command_args[0].lower(), message.mentions, message.author.id)
    if command == f'{prefix}clear':
        await clear_chat(channel)
    if command == f'{prefix}watchtime':
        # TODO change watchtime method
        await calculate_watchtime()
    else:
        pass


bot.run(TOKEN)
