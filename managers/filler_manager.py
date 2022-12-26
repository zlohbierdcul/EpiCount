from managers.file_manager import read_data


def check_if_filler(current_episode, key):
    data = read_data('data/data.json')
    is_filler = False
    last_filler = 0
    episodes_till_last_filler = 0
    for x in data[key]['filler']:
        if len(x) > 1:
            if x[0] <= current_episode <= x[1]:
                is_filler = True
                last_filler = x[1]
                episodes_till_last_filler = last_filler - current_episode
        else:
            if x[0] == current_episode:
                is_filler = True
                last_filler = x[0]
                episodes_till_last_filler = last_filler - current_episode
    return [is_filler, last_filler, episodes_till_last_filler]