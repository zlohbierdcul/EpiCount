import os
import discord
from dotenv import load_dotenv

from managers.file_manager import read_data, write_data
from message import counter_sender
from util import link_generator, series_adder
from message.chat_clearer import clear_chat, messageid, countdown
from message.counter_remover import remove_counter
from managers.data_management import remove_entry
from managers.filler_manager import check_if_filler
from message.message_sender import send_message

load_dotenv()

# discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# ? Bot client configuration
intents = discord.Intents.all()
prefix = "!"
client = discord.Client(intents=intents, activity=discord.Game(name=f'prefix: {prefix}'))

channel_id = 1009556444246446210
channel = client.get_channel(channel_id)

ADMIN_USER_ID = [409486429392207873]
JSON_DATA_PATH = "data/data.json"
UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"

EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]


# ? Gets executed when the bot starts
@client.event
async def on_ready():
    guilds = client.guilds
    print(f"\n{client.user} is ready\nConnected to {len(guilds)} Server\n")
    on_ready_channel = client.get_channel(channel_id)
    await clear_chat(on_ready_channel)


async def reload_message(key):
    # TODO rewrite method
    data = read_data()
    awaited_channel = client.get_channel(channel_id)
    message_obj = await awaited_channel.fetch_message(messageid[key])
    filler_array = check_if_filler(data[key]['episode'], key)
    is_filler = filler_array[0]
    last_filler = filler_array[1]
    epi_till_last = filler_array[2]
    filler_message = f'Filler Folge! Ende: {last_filler}, noch {epi_till_last} Folgen!'
    no_filler_message = 'Keine Filler Folge!'
    embeded_message = discord.Embed(title=data[key]["name"],
                                    description=f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]} \n {filler_message if is_filler else no_filler_message}',
                                    color=discord.Color.from_rgb(0, 255, 0))
    await message_obj.edit(embed=embeded_message)
    await clear_chat(awaited_channel)


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
    data = read_data()
    data[key]["episode"] = int(num)
    write_data(data)
    await reload_message(key)


async def set_season(key, num):
    data = read_data()
    data[key]["season"] = int(num)
    write_data(data)
    await reload_message(key)


async def calculate_watchtime(watchtime_channel):
    data = read_data()
    watchtime = data["onepiece"]["episode"] * 20
    watchtime_hours = format_time(watchtime)
    embeded_message = discord.Embed(title="Watchtime",
                                    description=f'{watchtime} min or {watchtime_hours}\nhave been watched!',
                                    color=discord.Color.from_rgb(0, 0, 255))
    await watchtime_channel.send(embed=embeded_message)
    await countdown(10)


def get_key(message_id):
    for x in messageid:
        if message_id == messageid[x]:
            return x


async def handle_reaction(payload):
    data = read_data()

    reaction_channel = client.get_channel(channel_id)

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
        await send_message(channel=reaction_channel, title='Link to current Episode',
                           description=link_generator.get_link(key),
                           color=discord.Color.from_rgb(0, 250, 250), reactions=[])
        await countdown(10)


@client.event
async def on_raw_reaction_add(payload):
    global channel_id
    add_reaction_channel = client.get_channel(channel_id)

    if not payload.user_id == client.user.id:
        print(f'messageids: {messageid}')
        key = get_key(payload.message_id)

        message_obj = await add_reaction_channel.fetch_message(payload.message_id)
        user_obj = client.get_user(payload.user_id)
        await message_obj.remove_reaction(payload.emoji.name, user_obj)

        print(key)

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
            embeded_message = discord.Embed(title="Error", description=f'You´re not authorized to do that!',
                                            color=discord.Color.from_rgb(255, 0, 0))
            awaited_channel = client.get_channel(payload.channel_id)
            await awaited_channel.send(embed=embeded_message)
            await countdown(2)


@client.event
async def on_message(message):
    messager_id = message.author.id
    message_channel = client.get_channel(channel_id)

    if messager_id == client.user.id:
        return None

    command_message = message.content
    print(command_message)
    command_list = command_message.split()
    command = command_list.pop(0)
    command_args = command_list

    if command == f'{prefix}rmseries':
        await remove_entry(command_args[0].lower(), message_channel)
    if command == f'{prefix}counter':
        await clear_chat(message_channel)
        await counter_sender.send_counter(command_args[0].lower(), message_channel)
    if command == f'{prefix}rmcounter':
        await remove_counter(command_args[0].lower(), message_channel)
        await clear_chat(message_channel)
    if command == f'{prefix}add':
        series_adder.add_series(command_args[0], messager_id)
        await counter_sender.send_counter(command_args[0].lower(), message_channel)
    if command == f'{prefix}setep':
        await set_episode(command_args[0].lower(), command_args[1])
    if command == f'{prefix}setse':
        await set_season(command_args[0].lower(), command_args[1])
    if command == f'{prefix}clear':
        await clear_chat(message_channel)
    if command == f'{prefix}watchtime':
        await calculate_watchtime(message_channel)
    else:
        await countdown(2)


client.run(TOKEN)
