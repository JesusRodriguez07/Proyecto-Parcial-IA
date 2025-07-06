import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/explosion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 10  # frames que durará la explosión

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
