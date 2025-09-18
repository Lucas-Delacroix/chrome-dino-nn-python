import pygame

FRAME_DT = 16
COLOR_BG = (255,255,255)
COLOR_GROUND_LINE = (0,0,0)
COLOR_DINO = (0, 100, 0)
GROUND_LINE_OFFSET = 1
COLOR_OBSTACLE = (100, 0, 0)
FPS = 60

WINDOW_W = 800
WINDOW_H = 600
GROUND_Y = 400
DINO_W = 40
DINO_H = 40
POS_X = 50
DUCK_HEIGHT = 20
STAND_HEIGHT = DINO_H

OBSTACLE_X = 20
OBSTACLE_Y = 40
OBSTACLE_SPEED = 0.3
FIRST_OBSTACLE_X = 400
OBSTACLE_SPACING = 300
INITIAL_OBSTACLES = 3
OBSTACLE_RESPAWN_OFFSET = 50
OBSTACLE_RESPAWN_MIN = 100
OBSTACLE_RESPAWN_MAX = 400

GRAVITY = 0.0015
GROUND_TOLERANCE = 1
JUMP_VELOCITY = 0.5

class Dino:
    def __init__(self):
        self.x = POS_X
        self.y = GROUND_Y
        self.vy = 0
        self.width = DINO_W
        self.height = DINO_H
        self.is_ducking = False

    def update(self, dt):
        self.vy += GRAVITY * dt
        self.y += self.vy * dt
        if self.y > GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0

    def jump(self):
        if self.y >= GROUND_Y - GROUND_TOLERANCE:
            self.vy = -JUMP_VELOCITY

    def duck(self, on=True):
        self.is_ducking = on
        if on:
            self.height = 20
        else:
            self.height = 40

    def rect(self):
        return pygame.Rect(self.x, int(self.y) - self.height, self.width, self.height)
