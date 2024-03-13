
LINE_HORIZONTAL = (0,0,0)
FACE = (130,100,30)
LINE_VERTICAL = (0,0,0)

BALL = (250,250,250)
SHOT_TRACKER_COLOR = (0,0,250)
TRACKER_COLOR = (250,0,0)
GRAPPLING_COLOR = (40,100,40)

BULLET_COLOR = (200,200,0)
SPRAY_BULLET_COLOR = (200,200,0)

def norm(x):
    if x>255:
        return 255
    if x<0:
        return 0
    return x

def color_spread(s, depth, grad):
    for i in range(depth):
        t = set()
        for color in s:
            r, g, b = color
            R, G, B = grad
            
            t.add((norm(r+R),norm(g+G),norm(b+B)))
        s.update(t)
    return s

def rgb_spread(s, depth):
    grads = [(1,1,-2),(-2,1,1),(1,-2,1)]
    for g in grads:
        s = color_spread(s,depth, g)
    return s

# underworld
BLUE_ROCK = list(rgb_spread({(60,60,100)},5))
SILVER_SAND = list(color_spread({(170,170,170)},20,(1,1,1)))
UNDERWORLD = (SILVER_SAND, BLUE_ROCK)

# world
GROUND = list(rgb_spread({(130,80,20)},10))
GRASS = list(rgb_spread({(50,190,40)},10))
WORLD = (GRASS, GROUND)

# overworld
WHITE_MARBLE = list(color_spread({(200,200,200)},5,(10,10,10)))
ELECTRUM = list(color_spread({(230,220,120)},20,(2,2,1))) # [(240,225,125)]
OVERWORLD = (ELECTRUM, WHITE_MARBLE)


BACKGROUND = (100,0,0)


