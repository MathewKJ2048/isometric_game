import sys

X, Y, Z = 1024, 1024, 1000

import math
from pygame.math import Vector3
import random
from colors import *

M = []
random_matrix_face = [[int(random.random()*1000) for _ in range(X)] for _ in range(Y)]
random_matrix_up = [[int(random.random()*1000) for _ in range(X)] for _ in range(Y)]

START_POINT = Vector3(52,52,8)


def init_map():
    global M
    for i in range(X):
        M.append([])
        for j in range(Y):
            M[i].append([])
            z_max= 0
            M[i][j].append((-1,z_max))
    M[2][101].append((1,3))

    
    def log(x):
        if x%128 == 0 or x == 0:
            return 16
        if x%32 == 0:
            return 8
        if x%8 == 0:
            return 4
        if x%2 == 0:
            return 1
        return 0

    
    # return

    for i in range(129):
        for j in range(129):
            z1 = log(i)
            z2 = log(j)
            z = max(z1,z2)
            if z != 0:
                M[i][j].append((0,z))

    print(sys.getsizeof(M))
    


def get_map(i,j):
    global M
    if i>=0 and j>=0 and i< X and j < Y:
        return M[i][j] 
    return [(-math.inf,math.inf)]

def in_map(i, j):
    if i>=0 and j>=0:
        if i<X and j<Y:
            return True
    return False

def get_floor_z(r):
    i, j = round(r.x), round(r.y)
    for t in get_map(i,j):
        if t[0]<=r.z and r.z<=t[1]:
            return t[1]
    return r.z

def is_collided(r):
    global M
    i, j = round(r.x), round(r.y)
    for t in get_map(i,j):
        if t[0]<=r.z and r.z<=t[1]:
            return True
    return False

def collision_normals(r, radius):
    directions = [Vector3(1,0,0),Vector3(0,1,0),Vector3(0,0,1)]
    normals = []
    for d in directions:
        if is_collided(r+d*radius):
            normals.append(d*-1)
        elif is_collided(r-d*radius):
            normals.append(d)
    return normals



def color_policy(x,y,z_top):
    up, face = OVERWORLD
    u = pick(up, random_matrix_up[x][y])
    f = pick(face, random_matrix_face[x][y])
    return u, f, LINE_VERTICAL, LINE_HORIZONTAL

def pick(l, index):
    return l[index%len(l)]


def get_background():
    return BACKGROUND




