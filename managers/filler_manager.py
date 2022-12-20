filler_episodes = [[54, 60], [98, 99], [102], [131, 143], [196, 206], [220, 226], [279, 283], [291, 292], [303],
                   [317, 319], [326, 336], [382, 384], [406, 407], [426, 429], [457, 458], [492], [542], [575, 578],
                   [590], [626, 627], [747, 750], [780, 782], [895, 896], [907], [1029, 1030]]


def check_if_filler(current_episode):
    is_filler = False
    last_filler = 0
    episodes_till_last_filler = 0
    for x in filler_episodes:
        if len(x) > 1:
            if (current_episode >= x[0] and current_episode <= x[1]):
                is_filler = True
                last_filler = x[1]
                episodes_till_last_filler = last_filler - current_episode
        else:
            if x[0] == current_episode:
                is_filler = True
                last_filler = x[0]
                episodes_till_last_filler = last_filler - current_episode
    return [is_filler, last_filler, episodes_till_last_filler]


print(check_if_filler(143))
