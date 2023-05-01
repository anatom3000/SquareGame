import numpy as np

RESOLUTION = np.array([1280, 720])
MAX_FPS = 60
# BACKGROUND_COLOR = (38, 124, 254)
BACKGROUND_COLOR = (0, 0, 0)

OBJECT_COLOR = (255, 255, 255)
PLAYER_COLOR = (0, 255, 0)

PLAYER_SPEED = 300*0.9
PLAYER_GRAVITY = 2370
JUMP_VELOCITY = 2*np.sqrt(45*PLAYER_GRAVITY)
