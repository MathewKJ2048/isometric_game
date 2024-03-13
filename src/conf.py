height = 640
width = 640

max_frame_rate = 30

camera_angular_sensitivity = 0.001
camera_linear_senistivity  = 0.01

SPRING_DRAG = 0.01
AIR_DRAG = 0.001
FORCE = 0.000005
GRAVITY = 0.00001
FRICTION = FORCE/2

DIRECTION_SENSITIVITY = 0.003

JUMP_TIME = 1000

SCALE_SENSITIVITY = 0.1

grappling_hook_reel_sensitivity = 0.004
grappling_spring_drag = 0.1

DIFFERENTIAL_EQUATION_SLICE_LIMIT = 10

GRAPPLING_STIFFNESS = 0.0001


ball_radius = 0.08
direction_tracker_radius = ball_radius/4
distance_tracker = 2*ball_radius
shot_tracker_radius = ball_radius/4
distance_shot = 2*ball_radius
distances_shot = [1,2,3,4]
for i in range(len(distances_shot)):
    distances_shot[i]*=ball_radius

grappling_tip_radius = ball_radius/2
grappling_velocity = 0.01
grappling_string_number = 32
grappling_string_radius = ball_radius/4
grappling_hook_length_limit = 4

bullet_radius = ball_radius/2
bullet_velocity = grappling_velocity

bullet_fragment_radius = bullet_radius
bullet_fragment_velocity = bullet_velocity/2
bullet_fragment_spread = 3
bullet_fragmenmt_degradation = bullet_fragment_radius*bullet_fragment_velocity/bullet_fragment_spread

BULLET_FRAGMENTS = 16
