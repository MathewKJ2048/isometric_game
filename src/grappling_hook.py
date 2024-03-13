from conf import *
from render_object import *
from colors import *
from pygame.math import Vector3

LOCK = 0
RETURN = 1

class Grappling_hook:
    def __init__(self,ob,diff_r):
        self.state = []
        self.tail_ob = ob
        self.r = ob.r + diff_r
        self.v = (diff_r).normalize()*grappling_velocity
        self.natural_length = 0
    
    def lock(self):
        self.velocity = Vector3(0,0,0)
        self.state.append(LOCK)
        self.natural_length = self.get_length()

    def reel(self,x):
        self.natural_length+=x
        if self.natural_length < 0:
            self.natural_length = 0
        if self.natural_length > grappling_hook_length_limit:
            self.natural_length = grappling_hook_length_limit

    def render(self):
        s = [Render_object(self.r,grappling_tip_radius,GRAPPLING_COLOR)]
        for i in range(grappling_string_number):
            f = i/(grappling_string_number)
            r = self.tail_ob.r*(1-f) + self.r*f
            s.append(Render_object(r,grappling_string_radius,GRAPPLING_COLOR))
        return s

    def get_length(self):
        return (self.r-self.tail_ob.r).magnitude()

    def get_normal(self):
        return (self.r-self.tail_ob.r).normalize()

    def render_outline(self):
        return []

    def get_state():
        return self.state
