# scripts/enemigo_disparo.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
import math
from scripts.arbol_comportamiento import Accion
from scripts.bala import Bullet

class EnemigoDisparo(pygame.sprite.Sprite):
    sprite_cache = None

    def __init__(self, x, y, jugador, grupo_balas_global):
        super().__init__()
        if EnemigoDisparo.sprite_cache is None:
            EnemigoDisparo.sprite_cache = pygame.image.load("assets/sprites/enemy_shooter.png").convert_alpha()
        self.image = EnemigoDisparo.sprite_cache
        self.rect = self.image.get_rect(center=(x, y))

        self.jugador = jugador
        self.velocidad = 1.5
        self.balas = pygame.sprite.Group()
        self.balas_global = grupo_balas_global
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()

        self.arbol = Accion(self.comportamiento_general)

    def comportamiento_general(self):
        self.mover_hacia_jugador()
        self.intentar_disparar()

    def mover_hacia_jugador(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.rect.x += int(self.velocidad * dx / dist)
        self.rect.y += int(self.velocidad * dy / dist)

    def intentar_disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_disparo > 2000:
            self.disparar()
            self.tiempo_ultimo_disparo = ahora

    def disparar(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        angulo = math.atan2(dy, dx)
        velocidad = 5
        vx = math.cos(angulo) * velocidad
        vy = math.sin(angulo) * velocidad

        bala = Bullet(self.rect.centerx, self.rect.centery, vector=(vx, vy), image_path="assets/sprites/bullet_enemy.png")
        self.balas.add(bala)
        self.balas_global.add(bala)

    def update(self):
        self.arbol.ejecutar()
        self.balas.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.balas.draw(surface)

