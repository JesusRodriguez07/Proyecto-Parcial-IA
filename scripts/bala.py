# scripts/bala.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=None, vector=None, image_path=None):
        super().__init__()
        if image_path is None:
            image_path = "assets/images/bullet.png"

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 10
        self.direction = direction
        self.vector = vector  # (vx, vy) for enemies

    def update(self):
        if self.vector:
            self.rect.x += self.vector[0]
            self.rect.y += self.vector[1]
        elif self.direction:
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

        if (self.rect.bottom < 0 or self.rect.top > 600 or
            self.rect.right < 0 or self.rect.left > 800):
            self.kill()
