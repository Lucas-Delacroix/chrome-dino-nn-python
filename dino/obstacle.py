import pygame

OBSTACLE_X = 20
OBSTACLE_Y = 40
OBSTACLE_SPEED = 0.3
GROUND_Y = 400

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = OBSTACLE_X
        self.height = OBSTACLE_Y
        self.speed = OBSTACLE_SPEED

    def update(self, dt):
        self.x -= self.speed * dt

    def rect(self):
        return pygame.Rect(int(self.x), GROUND_Y - self.height, self.width, self.height)