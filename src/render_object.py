import pygame

class Render_object:
    def __init__(self,r,radius,color,width=0,substantial=False):
        self.r = r
        self.color = color
        self.width = width
        self.radius = radius
        self.subtantial = substantial
    def render(self,surface,coordinates,scale):
        pygame.draw.circle(surface,self.color,coordinates,scale*self.radius,self.width)