from ball import *
from grappling_hook import *
from pygame.math import Vector3
from conf import *
from bullet import *


ball = Ball(START_POINT)

grp = None

bullets = []
particles = []

def shoot():
    global bullets
    global ball
    bullets.append(Bullet(ball.r,ball.get_shot_vector()*bullet_velocity))

def evolve_bullet(bt, dt):
    global particles
    if is_collided(bt.r) or (get_game_time() - bt.init_time > 1000):
        bt.deactivate()
        particles+=bt.get_particle_effect()
    bt.r += bt.v*dt

def get_active_objects():
    answer = [get_ball()]
    if grp:
        answer.append(grp)
    for bt in bullets:
        answer.append(bt)
    for p in particles:
        answer.append(p)
    return answer

def deploy_grappling_hook():
    global grp, ball
    if grp:
        grp = None
        return
    grp = Grappling_hook(ball,ball.get_shot_vector()*distance_shot)

def get_ball():
    global ball
    return ball

def reel_grappling_hook(x,dt):
    global grp
    if grp:
        grp.reel(x*grappling_hook_reel_sensitivity*dt)

def evolve_grappling_hook(dt):
    global grp
    if LOCK in grp.state:
        if grp.get_length() > grp.natural_length:
            grp.tail_ob.a += grp.get_normal()*(grp.get_length()-grp.natural_length)*GRAPPLING_STIFFNESS - grp.tail_ob.v.project(grp.get_normal())*SPRING_DRAG
        return

    # unlocked

    if RETURN in grp.state:
        grp.v = grp.get_normal()*-grappling_velocity
    
    r_new = grp.r + grp.v*dt

    if is_collided(r_new):
        grp.lock()

    grp.r = r_new
    if grp.get_length() > grappling_hook_length_limit:
        grp.state.append(RETURN)
    
    if grp.get_length() < distance_shot:
        grp = None


def evolve_ball(b, dt):
    # noclip stopper
    LIMIT = 2*b.radius
    disp = (b.v*dt).magnitude()
    if disp >= LIMIT:
        b.v = b.v.normalize()*LIMIT/dt

    r_new = b.r + b.v*dt

    cn = collision_normals(r_new, b.radius)
    down = r_new+Vector3(0,0,-1)*b.radius
    r_new.z = get_floor_z(down)+b.radius
    def closest_boundary(n):
        return round(2*n)/2
    for n in cn:
        coll_point = r_new - n*b.radius
        if n.x != 0:
            coll_point.x = closest_boundary(coll_point.x)
        if n.y != 0:
            coll_point.y = closest_boundary(coll_point.y)
        r_new = coll_point + n*b.radius
    

    v_new = b.v + Vector3(0,0,-1)*GRAVITY*dt+b.a*dt - b.v*AIR_DRAG*dt
    friction = False
    for n in cn:
        if n.z == 1:
            friction = True
        
            
    if friction:
        friction_term = FRICTION*dt
        v_new_xy = Vector3(v_new.x, v_new.y,0)
        if v_new_xy.magnitude() != 0:
            v_new -= v_new_xy.normalize()*min(friction_term,v_new_xy.magnitude())
                

    if b.jump_time > 0:
        time = JUMP_TIME - b.jump_time
        v_new.z = (GRAVITY*JUMP_TIME/2 - GRAVITY*time)
        b.jump_time -= dt


    for n in cn:
        f = n.dot(v_new)
        if f < 0:
            v_new-=1*n*f

    b.r = r_new
    b.v = v_new
    b.a = Vector3(0,0,0)


def evolve_particle(p, dt):
    p.r+=p.v*dt
    p.v+=Vector3(0,0,-1)*GRAVITY*dt

def evolve(dt):
    global ball, grp, bullets, particles
    increment_game_time(dt)
    if grp:
        evolve_grappling_hook(dt)
    evolve_ball(ball, dt)
    for bt in bullets:
        evolve_bullet(bt,dt)
    for p in particles:
        evolve_particle(p, dt)

    for bt in bullets:
        if not bt.active:
            bullets.remove(bt)
    for p in particles:
        if p.get_radius() <= 0:
            particles.remove(p)


def jump():  
    global ball
    for n in collision_normals(ball.r,ball.radius):
            if n.z == 1:
                ball.jump_time = JUMP_TIME
                return
    if grp:
        if grp.r.z > ball.r.z:
            ball.jump_time = JUMP_TIME
    
