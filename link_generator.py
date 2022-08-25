import discord
import json

JSON_DATA_PATH = "/Users/lucdreibholz/GitHub/BotiBot/2wnty1ne-Discord-Bot/data/data.json"

episodes_per_season = [ 61, 16, 15, 38, 13, 52, 33, 35, 73, 45, 26, 14, 35, 60, 57, 55, 118, 36, 107, 124, 16 ]


def calculate_link_episode():
    with open(JSON_DATA_PATH) as f:
        data = json.load(f)

    current_episode = data["onepiece"]["episode"]
    episodes_till_season = calculate_episodes_till_season(data)


    link_episode = current_episode - episodes_till_season

    print(f'link_episode: {link_episode}')

    return link_episode

def calculate_episodes_till_season(data):
    current_season = data["onepiece"]["season"]
    episodes_till_season = 0
    for x in range(current_season - 1):
        print(f'x : {x}')
        episodes_till_season += episodes_per_season[x]
    print(f'episodes_till_season: {episodes_till_season}')
    return episodes_till_season

