# dino_game.py
import pygame
import random
import math

WINDOW_W = 800
WINDOW_H = 600
GROUND_Y = 400

class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_Y
        self.vy = 0
        self.width = 40
        self.height = 40
        self.is_ducking = False

    def update(self, dt):
        # gravidade
        self.vy += 0.0015 * dt
        self.y += self.vy * dt
        if self.y > GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0

    def jump(self):
        if self.y >= GROUND_Y - 1:
            self.vy = -0.5

    def duck(self, on=True):
        self.is_ducking = on
        if on:
            self.height = 20
        else:
            self.height = 40

    def rect(self):
        return pygame.Rect(self.x, int(self.y) - self.height, self.width, self.height)

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = 20
        self.height = 40
        self.speed = 0.3

    def update(self, dt):
        self.x -= self.speed * dt

    def rect(self):
        return pygame.Rect(int(self.x), GROUND_Y - self.height, self.width, self.height)

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
        self.obstacles = [Obstacle(400 + i*300) for i in range(3)]
        self.t = 0
        self.done = False
        self.score = 0
        return self._get_sensors()

    def step(self, action, dt=16):
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
            if obs.x + obs.width < -50:
                obs.x = WINDOW_W + random.randint(100, 400)
                obs.height = random.choice([20,40,60])
                obs.width = random.randint(20,40)

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
        self.screen.fill((255,255,255))
        pygame.draw.line(self.screen, (0,0,0), (0, GROUND_Y+1), (WINDOW_W, GROUND_Y+1))
        pygame.draw.rect(self.screen, (0,100,0), self.dino.rect())
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (100,0,0), obs.rect())
        font = pygame.font.SysFont(None, 24)
        img = font.render(f"Score: {int(self.score)}", True, (0,0,0))
        self.screen.blit(img, (10,10))
        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    env = DinoEnv(render=True)
    s = env.reset()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        # controle humano
        keys = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_SPACE]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2
        s, score, done, _ = env.step(action, dt=16)
        env.render_frame()
        if done:
            print("Morreu! Score:", score)
            env.reset()
    pygame.quit()
