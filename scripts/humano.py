# scripts/humano.py
# Autor: jesus rodriguez - 12-sisn-2-043

# scripts/humano.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame

class Humano(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/human.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
