import pygame
from dino.assets import load_image, scale_image

WINDOW_W = 800
WINDOW_H = 600
GROUND_Y_RATIO = 0.9
GROUND_Y = int(WINDOW_H * GROUND_Y_RATIO)
DINO_W = 40
DINO_H = 40
POS_X = 50
JUMP_VELOCITY = 0.5
DUCK_HEIGHT = 20
STAND_HEIGHT = DINO_H

GRAVITY = 0.0015
GROUND_TOLERANCE = 1



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
