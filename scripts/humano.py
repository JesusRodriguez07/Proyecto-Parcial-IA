# scripts/humano.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
import random

class Humano(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/human.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.direccion = random.choice(['up', 'down', 'left', 'right', 'stay'])
        self.velocidad = 1
        self.timer_cambio = pygame.time.get_ticks()

    def update(self):
        ahora = pygame.time.get_ticks()

        # Cambiar dirección aleatoria cada 1.5 segundos
        if ahora - self.timer_cambio > 1500:
            self.direccion = random.choice(['up', 'down', 'left', 'right', 'stay'])
            self.timer_cambio = ahora

        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

        # No salirse de la pantalla
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
