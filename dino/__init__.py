import pygame
import random
from dino.dino import Dino
from dino.obstacle import Obstacle


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




class DinoEnv:
    def __init__(self, render=False):
        self.render = render
        if render:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
            pygame.display.set_caption("Dino (minimal)")
            self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = [Obstacle(FIRST_OBSTACLE_X + i*OBSTACLE_SPACING) for i in range(INITIAL_OBSTACLES)]
        self.t = 0
        self.done = False
        self.score = 0
        return self._get_sensors()

    def step(self, action, dt=FRAME_DT):
        """
        action: 0 = nada, 1 = pular, 2 = abaixar
        dt: ms since last frame
        """
        if action == 1:
            self.dino.jump()
        elif action == 2:
            self.dino.duck(True)
        else:
            self.dino.duck(False)

        self.dino.update(dt)

        for obs in self.obstacles:
            obs.update(dt)
            # Quanto o obstaculo passou da tela e pode ser
            # Reposicionado
            if obs.x + obs.width < - OBSTACLE_RESPAWN_OFFSET:
                obs.x = WINDOW_W + random.randint(OBSTACLE_RESPAWN_MIN, OBSTACLE_RESPAWN_MAX)

        # colisão?
        for obs in self.obstacles:
            if self.dino.rect().colliderect(obs.rect()):
                self.done = True

        self.t += dt
        self.score += dt

        sensors = self._get_sensors()
        return sensors, self.score, self.done, {}

    def _get_sensors(self):
        # pega o obstáculo mais próximo à direita do dino
        obstacles_sorted = sorted([o for o in self.obstacles if o.x + o.width > self.dino.x], key=lambda o: o.x)
        if obstacles_sorted:
            next_o = obstacles_sorted[0]
            dist = (next_o.x - self.dino.x) / WINDOW_W  # normalizado
            o_h = next_o.height / WINDOW_H
            o_w = next_o.width / WINDOW_W
        else:
            dist, o_h, o_w = 1.0, 0.0, 0.0

        dino_y = (GROUND_Y - self.dino.y) / WINDOW_H  # quanto está no ar
        dino_v = self.dino.vy  # pode normalizar mais se quiser
        is_duck = 1.0 if self.dino.is_ducking else 0.0

        # retornamos 6 sensores (sem bias): [dist, o_h, o_w, dino_y, dino_v, is_duck]
        return [dist, o_h, o_w, dino_y, dino_v, is_duck]

    def render_frame(self):
        if not self.render:
            return
        self.screen.fill(COLOR_BG)
        pygame.draw.line(self.screen, COLOR_GROUND_LINE, (0, GROUND_Y+GROUND_LINE_OFFSET), (WINDOW_W, GROUND_Y+GROUND_LINE_OFFSET))
        pygame.draw.rect(self.screen, COLOR_DINO, self.dino.rect())
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, obs.rect())
        font = pygame.font.SysFont(None, 24)
        img = font.render(f"Score: {int(self.score)}", True, (0,0,0))
        self.screen.blit(img, (10,10))
        pygame.display.flip()
        self.clock.tick(FPS)

