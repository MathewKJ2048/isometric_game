from pygame.math import Vector3
from game_map import *
from render_object import *
from conf import *
import pygame

class Ball:
    def __init__(self,r):
        self.r = r
        self.v = Vector3(0,0,0)
        self.a = Vector3(0,0,0)
        self.radius = 0.08
        self.direction_angle = 0
        self.shot_angle_theta = 0
        self.shot_angle_phi = 0
        self.jump_time = 0

    def get_direction_vector(self):
        return Vector3(math.cos(self.direction_angle),math.sin(self.direction_angle),0)

    def get_tracker(self):
        return self.r+self.get_direction_vector()*distance_tracker
    
    def get_shot_vector(self):
        ct = math.cos(self.shot_angle_theta)
        st = math.sin(self.shot_angle_theta)
        cp = math.cos(self.shot_angle_phi)
        sp = math.sin(self.shot_angle_phi)
        i, j ,k = Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,1)
        return (i*ct*sp + j*sp*st + k*cp)
    
    def get_shot(self):
        return self.r+self.get_shot_vector()*distance_shot
    
    def render_outline(self):
        return [Render_object(self.r,self.radius,(0,0,0),width=1)]
    
    def render(self):
        answer = [Render_object(self.r,self.radius,BALL,substantial=True),
        Render_object(self.get_tracker(),direction_tracker_radius,TRACKER_COLOR)]
        for d in distances_shot:
            answer.append(Render_object(self.r+self.get_shot_vector()*d,shot_tracker_radius,SHOT_TRACKER_COLOR))
        return answer

    

    def rotate_direction_vector(self,omega,dt):
        self.direction_angle+=omega*dt*DIRECTION_SENSITIVITY

    def rotate_shot_vector_theta(self,omega,dt):
        self.shot_angle_theta+=omega*dt*DIRECTION_SENSITIVITY
    
    def rotate_shot_vector_phi(self,omega,dt):
        self.shot_angle_phi+=omega*dt*DIRECTION_SENSITIVITY
        if self.shot_angle_phi<0:
            self.shot_angle_phi = 0
        if self.shot_angle_phi>math.pi:
            self.shot_angle_phi = math.pi

    def accelerate_ball(self,a,dt):
        self.a = self.get_direction_vector()*FORCE*a
