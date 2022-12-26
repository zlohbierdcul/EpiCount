import re

from managers.file_manager import read_data

episodes_per_season = [61, 16, 15, 38, 13, 52, 33, 35, 73, 45, 26, 14, 35, 60, 57, 55, 118, 36, 107, 124, 16]


def get_link(key):
    # TODO implement method
    data = read_data('data/data.json')
    link = data[key]["link"]

    print(link)
    #formatted_link = link.format(episode=str(data[key]["episode"]), season=str(data[key]["season"]))
    try:
        match = re.search(r"{episode([+|-])(\d+)}", link)
        operator = match.group(1)
        value = match.group(2)
        episode = eval(str(data[key]["episode"]) + operator + value)
        link = link.replace(f"{{episode{operator}{value}}}", str(episode))
    except Exception:
        link = link.replace("{episode}", str(data[key]["episode"]))
    try:
        link.replace("{season}", str(data[key]["season"]))
    except Exception:
        print("Cannot replace season!")
    return link


def calculate_link_episode(key):
    data = read_data('data/data.json')
    current_episode = data[key]["episode"]
    episodes_till_season = calculate_episodes_till_season(data, key)

    link_episode = current_episode - episodes_till_season

    print(f'link_episode: {link_episode}')

    return link_episode


def calculate_episodes_till_season(data, key):
    current_season = data[key]["season"]
    episodes_till_season = 0
    for x in range(current_season - 1):
        print(f'x : {x}')
        episodes_till_season += data[key]['episodes_per_season'][x]
    print(f'episodes_till_season: {episodes_till_season}')
    return episodes_till_season
