import asyncio
import os
import discord
from dotenv import load_dotenv

from managers.file_manager import read_data, write_data
from message import counter_sender
from message.counter_sender import create_counter_embeded
from message.send_error import send_error
from util import link_generator, series_adder
from message.chat_clearer import clear_chat, messageid, countdown
from message.counter_remover import remove_counter
from managers.data_management import remove_entry
from managers.filler_manager import check_if_filler
from message.message_sender import send_message, create_embeded
from util.link_generator import get_link

load_dotenv()

# discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# ? Bot client configuration
intents = discord.Intents.all()
prefix = "!"
client = discord.Client(intents=intents, activity=discord.Game(name=f'prefix: {prefix}'))

channel_id = 1055253364759351336

ADMIN_USER_ID = [409486429392207873]

UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"

EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]


# ? Gets executed when the bot starts
@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    guilds = client.guilds
    print(f"\n{client.user} is ready\nConnected to {len(guilds)} Server\n")
    await clear_chat(channel)


async def reload_message(key):
    channel = client.get_channel(channel_id)
    message_obj = await channel.fetch_message(messageid[key])
    await message_obj.edit(embed=create_counter_embeded(key))
    await clear_chat(channel)


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


async def set_episode(key, num):
    channel = client.get_channel(channel_id)
    data = read_data()
    try:
        data[key]["episode"] = int(num)
    except Exception:
        await send_error("The series does not exist!", "Please enter a valid series!", channel)
    write_data(data)
    await reload_message(key)


async def set_season(key, num):
    channel = client.get_channel(channel_id)
    data = read_data()
    try:
        data[key]["season"] = int(num)
    except Exception:
        await send_error("The series does not exist!", "Please enter a valid series!", channel)
    write_data(data)
    await reload_message(key)


async def calculate_watchtime(watchtime_channel):
    channel = client.get_channel(channel_id)
    data = read_data()
    watchtime = data["onepiece"]["episode"] * 20
    watchtime_hours = format_time(watchtime)
    embeded_message = discord.Embed(title="Watchtime",
                                    description=f'{watchtime} min or {watchtime_hours}\nhave been watched!',
                                    color=discord.Color.from_rgb(0, 0, 255))
    message = await watchtime_channel.send(embed=embeded_message)
    await asyncio.sleep(10)
    await message.delete()


def get_key(message_id):
    for x in messageid:
        if message_id == messageid[x]:
            return x


async def handle_reaction(payload):
    channel = client.get_channel(channel_id)
    data = read_data()
    key = get_key(payload.message_id)

    if payload.emoji.name == UP_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] + 1
    if payload.emoji.name == DOWN_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] - 1
    if payload.emoji.name == PLUS_EMOJI:
        data[key]["season"] = data[key]["season"] + 1

    write_data(data)
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


@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(channel_id)

    if not payload.user_id == client.user.id:
        print(f'messageids: {messageid}')
        key = get_key(payload.message_id)

        message_obj = await channel.fetch_message(payload.message_id)
        user_obj = client.get_user(payload.user_id)
        await message_obj.remove_reaction(payload.emoji.name, user_obj)

        def check_auth():
            data = read_data()
            if payload.user_id in data[key]['auth_id'] or payload.user_id in ADMIN_USER_ID:
                return True
            else:
                return False

        admin_or_link = check_auth() or (payload.emoji.name == LINK_EMOJI)
        if (payload.channel_id == channel_id) and admin_or_link and not (payload.user_id == client.user.id):
            await handle_reaction(payload)
        elif not payload.user_id == client.user.id:
            awaited_channel = client.get_channel(payload.channel_id)
            message = await send_error("You´re not authorized to do that!", "Fuck off now!", awaited_channel)
            await asyncio.sleep(2)
            await message.delete()


@client.event
async def on_message(message):
    print(messageid)
    messager_id = message.author.id
    channel = client.get_channel(channel_id)

    if messager_id == client.user.id or message.content is None:
        return None

    await message.delete()
    command_message = message.content
    command_list = command_message.split()
    command = command_list.pop(0)
    command_args = command_list

    if command == f'{prefix}rmseries':
        await remove_entry(command_args[0].lower(), channel)
    if command == f'{prefix}counter':
        # await clear_chat(channel)
        await counter_sender.send_counter(channel, command_args[0].lower())
    if command == f'{prefix}rmcounter':
        await remove_counter(command_args[0].lower(), channel)
        await clear_chat(channel)
    if command == f'{prefix}add':
        await series_adder.add(channel, command_args[0], messager_id, client)
    if command == f'{prefix}setep':
        await set_episode(command_args[0].lower(), command_args[1])
    if command == f'{prefix}setse':
        await set_season(command_args[0].lower(), command_args[1])
    if command == f'{prefix}clear':
        await clear_chat(channel)
    if command == f'{prefix}watchtime':
        # TODO change watchtime method
        await calculate_watchtime(channel)
    else:
        pass


client.run(TOKEN)
