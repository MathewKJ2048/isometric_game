from conf import *
from render_object import *
from colors import *
from pygame.math import Vector3
from particle import *

class Bullet:
    def __init__(self,r,v):
        self.r = r
        self.v = v
        self.radius = bullet_radius
        self.color = BULLET_COLOR
        self.active = True
        self.init_time = get_game_time()

    def deactivate(self):
        self.active = False
    
    def render(self):
        return [Render_object(self.r,self.radius, self.color, substantial=False),Render_object(self.r,self.radius, (0,0,0), substantial=False, width=1)]
    
    def render_outline(self):
        return []

    def get_particle_effect(self):
        particles = []
        r_s = random_spherical_vectors(bullet_fragment_velocity, BULLET_FRAGMENTS)
        for t in r_s:
            particles.append(Particle(self.r, t, SPRAY_BULLET_COLOR, bullet_fragment_radius,bullet_fragmenmt_degradation))
        return particles