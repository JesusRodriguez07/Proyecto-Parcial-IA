# scripts/humano.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
import random

# Clase Humano: representa a los civiles que el jugador debe rescatar
class Humano(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Inicializa como sprite de Pygame

        # Carga el sprite del humano con transparencia
        self.image = pygame.image.load("assets/sprites/human.png").convert_alpha()

        # Posiciona al humano en el punto (x, y)
        self.rect = self.image.get_rect(center=(x, y))

        # Dirección inicial aleatoria (puede quedarse quieto también)
        self.direccion = random.choice(['up', 'down', 'left', 'right', 'stay'])

        self.velocidad = 1  # Velocidad de movimiento constante

        # Temporizador para cambiar de dirección cada cierto tiempo
        self.timer_cambio = pygame.time.get_ticks()

    # Método que se ejecuta en cada frame
    def update(self):
        ahora = pygame.time.get_ticks()

        # Cambia de dirección cada 1.5 segundos
        if ahora - self.timer_cambio > 1500:
            self.direccion = random.choice(['up', 'down', 'left', 'right', 'stay'])
            self.timer_cambio = ahora

        # Movimiento en la dirección actual
        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

        # Limita el movimiento para que no se salga de la pantalla (800x600)
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

