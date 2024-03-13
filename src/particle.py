from conf import *
from render_object import *
from colors import *
from pygame.math import Vector3
from game_clock import *
import random


class Particle:
    def __init__(self,r,v,color,radius_init,degrade_rate):
        self.r = Vector3(r.x,r.y,r.z)
        self.v = Vector3(v.x,v.y,v.z)
        self.radius = radius_init
        self.color = color
        self.init_time = get_game_time()
        self.degrade_rate = degrade_rate

    def get_radius(self):
        rad = self.radius - (get_game_time()-self.init_time)*self.degrade_rate
        return max(rad, 0)
    
    def render(self):
        return [Render_object(self.r,self.get_radius(), self.color, substantial=False),Render_object(self.r,self.get_radius(), (0,0,0),width=1, substantial=False)]
    
    def render_outline(self):
        return []


def random_spherical_vectors(velocity,number):
    s = []
    for i in range(number):
        v = Vector3(random.random()-0.5,random.random()-0.5,random.random()-0.5)
        s.append(v.normalize()*velocity)
    return s
