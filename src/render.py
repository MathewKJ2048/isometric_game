import pygame
from pygame.math import Vector3
from conf import *
from game_map import *
from ball import *
from board import *
from render_object import *


X_camera = 3
Y_camera = 3
Z_camera = 10

scale = 100

show_info = True

def toggle_info():
    global show_info
    show_info = not show_info


ERROR = 2*scale

theta = -3*math.pi/4
phi = math.pi/4



def get_n():
    global theta
    global phi
    ct = math.cos(theta)
    st = math.sin(theta)
    cp = math.cos(phi)
    sp = math.sin(phi)
    return Vector3(ct*sp, st*sp, cp)
n = get_n()
def get_bases():
    global n
    i, j, k = Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,1)
    def proj(v, n):
        return v - n*v.dot(n)
    I, J, K = proj(i,n), proj(j,n), proj(k,n)
    p = K.normalize()
    q = p.cross(n)
    return (I,J,K), (p,q)
basis3, basis2 = get_bases()

def rotate_theta(s):
    global theta
    global n
    global basis2, basis3
    theta+=s
    n = get_n()
    basis3, basis2 = get_bases()
def rotate_phi(s):
    global phi
    global n
    global basis2, basis3
    phi+=s
    if phi <= 0.01:
        phi = 0.01
    if phi >= math.pi/2:
        phi = math.pi/2 - 0.01
    n = get_n()
    basis3, basis2 = get_bases()
    


camera = Vector3(0,0,0)
def move_camera(x,y,z):
    global camera
    camera = camera + Vector3(x,y,z)

def camera_coordinates():
    global camera
    return round(camera.x), round(camera.y), round(camera.z)


def transform(v):
    global camera
    v = v-camera
    a, b, c = v.x, v.y, v.z
    global basis2, basis3
    I, J, K = basis3
    p, q = basis2
    v_ = I*a + J*b + K*c
    X, Y = v_.dot(q), v_.dot(p)
    return width/2+scale*X, height/2-scale*Y

def key(v):
    global n
    return n.x*v[0]+n.y*v[1]

def in_limits(t_point):
    x, y = t_point[0], t_point[1]
    return -ERROR<=x and x<=width+ERROR and -ERROR<=y and y<=height+ERROR
def vertical_offset(t_point):
    x, y = t_point[0], t_point[1]
    if y<=-ERROR:
        y=-ERROR
    elif y>=height+ERROR:
        y = height+ERROR
    return (x,y)
def polygonize(coordinates,map_element):
    i, j = coordinates
    z_, z = map_element
    points = [(i+0.5,j+0.5),(i+0.5,j-0.5),(i-0.5,j-0.5),(i-0.5,j+0.5)]
    ci, cj = camera.x, camera.y
    def truncate(val, lim):
        if val>lim:
            return lim
        if val<-lim:
            return -lim
        return val
    for g in range(len(points)):
        i, j = points[g]
        rel_i, rel_j = i-ci, j-cj
        rel_i = truncate(rel_i,X_camera)
        rel_j = truncate(rel_j,Y_camera)
        points[g] = (ci+rel_i,cj+rel_j)

        
    points.sort(key=key)
    def up(p):
        x, y = p
        return transform(Vector3(x,y,z))
    def down(p):
        x, y = p
        return transform(Vector3(x,y,z_))
    up_vectors = [up(p) for p in points]
    down_vectors = [down(p) for p in points]
    return up_vectors, down_vectors

def draw(surface,coordinates,map_element,truncate_z = False):

    up_color, face_color, line_vertical_color, line_horizontal_color = color_policy(coordinates[0], coordinates[1], map_element[0])
    
    if truncate_z:
        up_color = face_color
        line_horizontal_color = line_vertical_color

    up_vectors, down_vectors = polygonize(coordinates, map_element)
    cric_perm = [3,2,0,1]
    def draw_side_poly(surface, t_points):
        pygame.draw.polygon(surface, face_color, [vertical_offset(tp) for tp in t_points])
    pygame.draw.polygon(surface,up_color,[up_vectors[cric_perm[i]] for i in range(4)])
    draw_side_poly(surface, [up_vectors[3],up_vectors[2],down_vectors[2],down_vectors[3]])
    draw_side_poly(surface, [up_vectors[3],up_vectors[1],down_vectors[1],down_vectors[3]])
    
    if not truncate_z or True:
        for i in range(4):
            pygame.draw.aaline(surface, line_horizontal_color, up_vectors[cric_perm[i-1]], up_vectors[cric_perm[i]])
    for i in [3,2,1]:
        pygame.draw.aaline(surface, line_vertical_color, vertical_offset(up_vectors[i]), vertical_offset(down_vectors[i]))
    for i in [2,1]:
        pygame.draw.aaline(surface, line_vertical_color, down_vectors[3], down_vectors[i])
    



def in_camera_zone(r):
        rel = r-camera
        x, y, z = rel.xyz
        return abs(x)<X_camera and abs(y)<Y_camera and abs(z)<Z_camera



def render(fps):
    global camera
    global n

    surface = pygame.Surface((width, height))

    X_camera, Y_camera, Z_camera = get_camera_limits()
    camera = get_ball().r
    ci, cj, cz = camera_coordinates()

    step_i = 1 if n.x > 0 else -1
    step_j = 1 if n.y > 0 else -1

    game_objects = get_active_objects()
    active_renders = []
    passive_renders = []
    for go in game_objects:
        active_renders+=(go.render())
        passive_renders+=(go.render_outline())

    def sort_key(render_ob):
        return n.dot(render_ob.r)
    active_renders.sort(key=sort_key)
    passive_renders.sort(key=sort_key)
    


    render_hashmap = {}

    for b in active_renders:
        if not in_camera_zone(b.r):
            continue
        t = b.r
        ct = t-camera
        i,j = round(t.x), round(t.y)

        embedded = False
        for t_m in get_map(i,j):
            if t.z >= t_m[0] and t.z <= t_m[1]:
                embedded = True
        if embedded:
            continue

        if b.subtantial:
            neighbours = [(i,j+step_j),(i+step_i,j),(i+step_i,j+step_j)]
            def in_square(c_sq, r):
                x, y = c_sq
                return abs(r.x-x)<0.5+b.radius*0.9 and abs(r.y-y)<0.5+b.radius*0.9
            for c in neighbours:
                if in_square(c, t):
                    i, j = c
        
        if str(i)+"|"+str(j) not in render_hashmap:
            render_hashmap[str(i)+"|"+str(j)] = []
        render_hashmap[str(i)+"|"+str(j)].append(b)
    
    
    map_coordinates = []
    for I in range(-step_i*X_camera, step_i*(X_camera+1), step_i):
        for J in range(-step_j*Y_camera, step_j*(Y_camera+1), step_j):
            i = ci+I
            j = cj+J
            map_coordinates.append((i,j))

    for c in map_coordinates:
        i, j = c
        cell_active_render_list = []
        if str(i)+"|"+str(j) in render_hashmap:
            cell_active_render_list = render_hashmap[str(i)+"|"+str(j)]

        def draw_t(t):
            if t[1] == math.inf:
                return
            if t[1] > camera.z+Z_camera:
                draw(surface,c,(t[0],camera.z+Z_camera),truncate_z=True)
            else:
                draw(surface,c,t)

        for t in get_map(i,j):
            for i in range(len(cell_active_render_list)):
                car = cell_active_render_list[i]
                if car and car.r.z < t[0]:
                    car.render(surface,transform(car.r),scale)
                    cell_active_render_list[i] = None
            draw_t(t)
        for car in cell_active_render_list:
            if car:
                car.render(surface,transform(car.r),scale)
            
                
    for b in passive_renders:
        b.render(surface,transform(b.r),scale)


    if show_info:
        text = "("+str(ci)+","+str(cj)+","+str(cz)+")"+"  fps:"+str(int(fps))
        render_shrink_blit_text(text, surface)

    
    return surface
    

def change_scale(s):
    global scale
    scale+=s
    if scale<0:
        scale = 0


def get_camera_limits():
    return X_camera, Y_camera, Z_camera

def change_boundary_xy(s):
    global X_camera, Y_camera
    X_camera+=s
    Y_camera+=s
    if X_camera<1:
        X_camera = 1
    if Y_camera<1:
        Y_camera = 1

def change_boundary_z(s):
    global Z_camera
    Z_camera+=s
    if Z_camera<1:
        Z_camera = 1

def render_shrink_blit_text(text, target_surface):

    font = pygame.font.Font(None, 36)
    color = (255,255,255)
    text_surface = font.render(text, True, color)
    scaled_surface = pygame.transform.scale(text_surface, (int(text_surface.get_width()),
                                                           int(text_surface.get_height())))
    target_surface.blit(scaled_surface, (0, 0))


