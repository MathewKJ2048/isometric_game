time = 0

def get_game_time():
    global time
    return time

def increment_game_time(dt):
    global time
    time+=dt