import pygame

OBSTACLE_X = 20
OBSTACLE_Y = 40
OBSTACLE_SPEED = 0.3
GROUND_Y = 400

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = OBSTACLE_X
        self.height = OBSTACLE_Y
        self.speed = OBSTACLE_SPEED

    def update(self, dt):
        self.x -= self.speed * dt

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y) - self.height, self.width, self.height)