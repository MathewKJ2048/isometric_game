import pygame
import math
import random
import asyncio
from render import *
from conf import *
from game_map import *
from board import *
import cProfile
import pstats

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Iso")


screen.fill(get_background())
pygame.display.update()



c = pygame.time.Clock()
running = True

def init():
    init_map()
    pass

init()


a = 0
fps = max_frame_rate

def main():
    
    global running
    global c
    global screen
    global pygame
    global a
    global fps

    while running:

        b = get_ball()
        dt = c.tick(max_frame_rate)
        fps = c.get_fps()
        dt_=dt/DIFFERENTIAL_EQUATION_SLICE_LIMIT
        for i in range(DIFFERENTIAL_EQUATION_SLICE_LIMIT):
            b.accelerate_ball(a,dt_)
            evolve(dt_)
        screen.blit(render(fps),(0,0))

        a = 0
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            a+=1
        if pressed_keys[pygame.K_s]:
            a-=1
        if pressed_keys[pygame.K_d]:
            b.rotate_direction_vector(-1,dt)
        if pressed_keys[pygame.K_a]:
            b.rotate_direction_vector(1,dt)
        if pressed_keys[pygame.K_KP8]:
            b.rotate_shot_vector_phi(-1,dt)
        if pressed_keys[pygame.K_KP2]:
            b.rotate_shot_vector_phi(1,dt)
        if pressed_keys[pygame.K_KP6]:
            b.rotate_shot_vector_theta(-1,dt)
        if pressed_keys[pygame.K_KP4]:
            b.rotate_shot_vector_theta(1,dt)
        if pressed_keys[pygame.K_q]:
            move_camera(0,0,dt*camera_linear_senistivity)    
        if pressed_keys[pygame.K_e]:
            move_camera(0,0,-dt*camera_linear_senistivity) 
        if pressed_keys[pygame.K_UP]:
            rotate_phi(camera_angular_sensitivity*dt)   
        if pressed_keys[pygame.K_DOWN]:
            rotate_phi(-camera_angular_sensitivity*dt)   
        if pressed_keys[pygame.K_RIGHT]:
            rotate_theta(camera_angular_sensitivity*dt)   
        if pressed_keys[pygame.K_LEFT]:
            rotate_theta(-camera_angular_sensitivity*dt)  
        if pressed_keys[pygame.K_COMMA]:
            change_scale(SCALE_SENSITIVITY*dt) 
        if pressed_keys[pygame.K_m]:
            change_scale(-SCALE_SENSITIVITY*dt)
        if pressed_keys[pygame.K_KP_PLUS]:
            reel_grappling_hook(1,dt)
        if pressed_keys[pygame.K_KP_MINUS]:
            reel_grappling_hook(-1,dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    if pressed_keys[pygame.K_0]:
                        change_boundary_z(1)
                    else:
                        change_boundary_xy(1)
                if event.key == pygame.K_MINUS:
                    if pressed_keys[pygame.K_0]:
                        change_boundary_z(-1)
                    else:
                        change_boundary_xy(-1)
                if event.key == pygame.K_i:
                    toggle_info()
                if event.key == pygame.K_KP5:
                    deploy_grappling_hook()
                if event.key == pygame.K_KP3:
                    shoot()
                if event.key == pygame.K_SPACE:
                    jump()
        
        
        pygame.display.update()
        


pr = cProfile.Profile()
pr.enable()
main()


pr.disable()
ps = pstats.Stats(pr).strip_dirs().sort_stats('cumtime').get_stats_profile()

cell_size = 10
def cell(s):
    s = str(s)
    t = len(s)
    if t <= cell_size:
        return s+(cell_size-t)*" "
    else:
        return "*"


ttime = ps.total_tt
def percent_time(t):
    return str(int(10000*t/ttime)/100)+"%"

s = cell("ncalls")+cell("tottime")+cell("percent")+cell("percall")+cell("cumtime")+cell("percent")+cell("percall")+cell("info")
for key in ps.func_profiles:
    value = ps.func_profiles[key]
    info = key + " (in line "+str(value.line_number)+" of "+str(value.file_name)+")"
    s+="\n"+cell(value.ncalls)+cell(value.tottime)+cell(percent_time(value.tottime))+cell(value.percall_tottime)+cell(value.cumtime)+cell(percent_time(value.cumtime))+cell(value.percall_cumtime)+info

with open('test.txt', 'w+') as f:
    f.write(s)