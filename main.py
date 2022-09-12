import datetime
from email import message
from tabnanny import check
import time
import discord
import json
from filler_manager import check_if_filler

import link_generator 
import series_adder
import counter_sender
from message_sender import send_message
from chat_clearer import clear_chat, messageid
from counter_remover import remove_counter
from data_management import remove_entry


# discord bot token
TOKEN = "MTAwOTYxMDgyNzIwMjA1NjI4Mw.GpYF7-.TeOU8Ok6Hjly-61wJf5oyNI0rWiNiOe5Owz0UI"


#? Bot client configuration
intents = discord.Intents.all()
prefix = "!"
client = discord.Client(intents=intents, activity=discord.Game(name=f'prefix: {prefix}'))

channel_id = 1009556444246446210
channel = client.get_channel(channel_id)

ADMIN_USER_ID = 409486429392207873
JSON_DATA_PATH = "data/data.json"
UP_ARROW_EMOJI = "⬆️"
DOWN_ARROW_EMOJI = "⬇️"
PLUS_EMOJI = "⏏️"
LINK_EMOJI = "📟"

EMOJI_ARRAY = [UP_ARROW_EMOJI, DOWN_ARROW_EMOJI, PLUS_EMOJI, LINK_EMOJI]

with open(JSON_DATA_PATH) as f:
    data = json.load(f)


#? Gets executed when the bot starts
@client.event
async def on_ready():
    global messageid
    guilds = client.guilds
    print(f"\n{client.user} is ready\nConnected to {len(guilds)} Server\n")
    channel = client.get_channel(channel_id)
    await clear_chat(channel)

async def reload_message(key):
    awaited_channel = client.get_channel(channel_id)
    message_obj = await awaited_channel.fetch_message(messageid[key])
    filler_array = check_if_filler(data[key]['episode'])
    is_filler = filler_array[0]
    last_filler = filler_array[1]
    epi_till_last = filler_array[2]
    filler_message = f'Filler Folge! Ende: {last_filler}, noch {epi_till_last} Folgen!'
    no_filler_message = 'Keine Filler Folge!'
    embeded_message = discord.Embed(title=data[key]["name"], description=f'Aktuelle Folge: Staffel {data[key]["season"]} Folge {data[key]["episode"]} \n {filler_message if is_filler else no_filler_message}', color=discord.Color.from_rgb(0,255,0))
    await message_obj.edit(embed=embeded_message)
    await clear_chat(awaited_channel)
    with open(JSON_DATA_PATH, 'w') as g:
        json.dump(data, g)

def commands_to_lower(command_list):
    commandlist_lower = []
    for x in range(len(command_list)):
        commandlist_lower.append(command_list[x].lower())
    return commandlist_lower

async def countdown(s):
    no_message = False
 
    # Calculate the total number of seconds
    total_seconds = s
 
    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
 
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds = total_seconds)
        
        # Prints the time left on the timer
        print(timer, end="\r")
 
        # Delays the program one second
        time.sleep(1)
 
        # Reduces total time by one second
        total_seconds -= 1
 
    await clear_chat(client.get_channel(channel_id))

def format_time(minutes):
    hours_total = minutes // 60
    # Get additional minutes with modulus
    minutes_total = minutes % 60
    # Create time as a string
    time_string = "{} hours {} minutes".format(hours_total, minutes_total)
    return time_string

async def set_episode(key, num):
    data[key]["episode"] = int(num)
    with open(JSON_DATA_PATH, 'w') as g:
        json.dump(data, g)
    await reload_message(key)

async def set_season(key, num):
    data[key]["season"] = int(num)
    with open(JSON_DATA_PATH, 'w') as g:
        json.dump(data, g)
    await reload_message(key)

async def calculate_watchtime(channel):
    watchtime = data["onepiece"]["episode"] * 20
    watchtime_hours = format_time(watchtime)
    embeded_message = discord.Embed(title="Watchtime", description=f'{watchtime} min or {watchtime_hours}\nhave been watched!', color=discord.Color.from_rgb(0,0,255))
    nice_message = await channel.send(embed = embeded_message)

def get_key(message_id):
    
    for x in messageid:
        if message_id == messageid[x]:
            return x
        
        


async def handle_reaction(payload):
    channel = client.get_channel(channel_id)

    key = get_key(payload.message_id)

    if payload.emoji.name == UP_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] + 1
    if payload.emoji.name == DOWN_ARROW_EMOJI:
        data[key]["episode"] = data[key]["episode"] - 1
    if payload.emoji.name == PLUS_EMOJI:
        data[key]["season"] = data[key]["season"] + 1
    if payload.emoji.name == LINK_EMOJI:
        current_season = data[key]["season"]
        link_episode = link_generator.calculate_link_episode()
        await send_message(channel=channel, title='Link to current Episode', description=f'https://burningseries.tw/serie/One-Piece/{current_season}/{link_episode}-Episode/de', color=discord.Color.from_rgb(0,250,250), reactions=[])
        await countdown(10)

    await reload_message(key)

    # embeded_message = discord.Embed(title=data[id]["name"], description=f'Aktuelle Folge: Staffel {data[id]["season"]} Folge {data[id]["episode"]}', color=discord.Color.from_rgb(0,255,0))
    # await message_obj.edit(embed=embeded_message)
    

    with open(JSON_DATA_PATH, 'w') as g:
        json.dump(data, g)


@client.event
async def on_raw_reaction_add(payload):
    global channel_id
    channel = client.get_channel(channel_id)

    if (not payload.user_id == client.user.id):
        print(f'messageids: {messageid}')
        key = get_key(payload.message_id)

        message_obj = await channel.fetch_message(payload.message_id)
        user_obj = client.get_user(payload.user_id)
        await message_obj.remove_reaction(payload.emoji.name, user_obj)

        print(key)
        def check_auth():
            if payload.user_id in data[key]['auth_id'] or payload.user_id == ADMIN_USER_ID:
                return True
            else:
                return False

            # for x in range(len(data[key]['auth_id'])):

            #     if payload.user_id == ADMIN_USER_ID or payload.user_id == data[key]['auth_id'][x]:
            #         return True
            #     else:
            #         return False

        admin_or_link = check_auth() or (payload.emoji.name == LINK_EMOJI)

        if (payload.channel_id == channel_id) and (admin_or_link) and not (payload.user_id == client.user.id):
            await handle_reaction(payload)
        elif not payload.user_id == client.user.id:
            embeded_message = discord.Embed(title="Error", description=f'You´re not authorized to do that!', color=discord.Color.from_rgb(255,0,0))
            awaited_channel = client.get_channel(payload.channel_id)
            nice_message = await awaited_channel.send(embed = embeded_message)
            await countdown(2)
        


    with open(JSON_DATA_PATH, 'w') as h:
        json.dump(data, h)

    
@client.event 
async def on_message(message):
    guild = message.guild
    messager_id = message.author.id
    channel = client.get_channel(channel_id)

    if messager_id == client.user.id:
        return None

    command_message = message.content
    print(command_message)
    command_list = command_message.split()
    command = command_list.pop(0)
    command_args = command_list

    if command == f'{prefix}rmseries':
        await remove_entry(command_args[0].lower(), channel)
    if command == f'{prefix}counter':
        await clear_chat(channel)
        await counter_sender.send_counter(command_args[0].lower(), channel)
    if command == f'{prefix}rmcounter':
        await remove_counter(command_args[0].lower(), channel)
        await clear_chat(channel)
    if command == f'{prefix}add':
        series_adder.add_series(command_args[0], messager_id)
        await counter_sender.send_counter(command_args[0].lower(), channel)
    if command == f'{prefix}setep':
        await set_episode(command_args[0].lower(), command_args[1])
    if command == f'{prefix}setse':
        await set_season(command_args[0].lower(), command_args[1])
    if command == f'{prefix}clear':
        await clear_chat(channel)
    if command == f'{prefix}watchtime':
        await calculate_watchtime(channel)
        await countdown(10)
    if command == f'{prefix}link':
        current_season = data["onepiece"]["season"]
        link_episode = link_generator.calculate_link_episode()
        await send_message(channel=channel, title='Link to current Episode', description=f'https://burningseries.tw/serie/One-Piece/{current_season}/{link_episode}-Episode/de', color=discord.Color.from_rgb(0,250,250), reactions=[])
        await countdown(10)
    else:
        await countdown(2)

    with open(JSON_DATA_PATH, 'r') as x:
        data = json.load(x)
        
    



client.run(TOKEN)