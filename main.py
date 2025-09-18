from dino import DinoEnv
import pygame
if __name__ == "__main__":
    env = DinoEnv(render=True)
    s = env.reset()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_SPACE]:
            action = 1
        elif keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2
        s, score, done, _ = env.step(action, dt=16)
        env.render_frame()
        if done:
            print("Morreu! Score:", score)
            env.reset()
    pygame.quit()
