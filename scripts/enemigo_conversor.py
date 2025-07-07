# scripts/enemigo_conversor.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
from scripts.a_estrella import a_estrella
from scripts.arbol_comportamiento import Selector, Secuencia, Condicion, Accion
from scripts.enemigo import Enemigo

class EnemigoConversor(Enemigo):
    sprite_converter = None

    def __init__(self, x, y, jugador, mapa, humanos, grupo_enemigos):
        super().__init__(x, y, jugador, mapa, humanos)
        self.grupo_enemigos = grupo_enemigos

        if EnemigoConversor.sprite_converter is None:
            EnemigoConversor.sprite_converter = pygame.image.load("assets/sprites/enemy_converter.png").convert_alpha()

        self.image = EnemigoConversor.sprite_converter
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        super().update()

        # Revisar si colisiona con un humano y convertirlo en enemigo
        if self.humanos:
            colisiones = pygame.sprite.spritecollide(self, self.humanos, dokill=True)
            for humano in colisiones:
                nuevo_enemigo = Enemigo(humano.rect.centerx, humano.rect.centery, self.jugador, self.mapa, self.humanos)
                nuevo_enemigo.velocidad = self.velocidad
                self.grupo_enemigos.add(nuevo_enemigo)
