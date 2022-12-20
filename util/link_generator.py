from managers.file_manager import read_data

episodes_per_season = [61, 16, 15, 38, 13, 52, 33, 35, 73, 45, 26, 14, 35, 60, 57, 55, 118, 36, 107, 124, 16]


def get_link(key):
    # TODO implement method
    pass


def calculate_link_episode(key):
    data = read_data()
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
