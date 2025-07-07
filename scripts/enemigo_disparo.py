# scripts/enemigo_disparo.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
import math
from scripts.arbol_comportamiento import Accion  # Usamos un nodo de acción simple del árbol de comportamiento
from scripts.bala import Bullet  # Importamos la clase Bullet para disparar proyectiles

# Clase EnemigoDisparo, un enemigo que persigue al jugador y dispara
class EnemigoDisparo(pygame.sprite.Sprite):
    sprite_cache = None  # Caché del sprite para que se cargue solo una vez

    def __init__(self, x, y, jugador, grupo_balas_global):
        super().__init__()  # Inicializa como un sprite de Pygame

        # Carga el sprite si aún no se ha cargado
        if EnemigoDisparo.sprite_cache is None:
            EnemigoDisparo.sprite_cache = pygame.image.load("assets/sprites/enemy_shooter.png").convert_alpha()

        self.image = EnemigoDisparo.sprite_cache
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial del enemigo

        self.jugador = jugador  # Referencia al jugador para seguirlo y dispararle
        self.velocidad = 1.5  # Velocidad de movimiento del enemigo

        self.balas = pygame.sprite.Group()  # Grupo local de balas que dispara este enemigo
        self.balas_global = grupo_balas_global  # Grupo global para que el juego pueda acceder a todas las balas

        self.tiempo_ultimo_disparo = pygame.time.get_ticks()  # Temporizador para controlar disparos

        # Nodo del árbol de comportamiento que ejecuta su lógica de combate
        self.arbol = Accion(self.comportamiento_general)

    # Comportamiento principal del enemigo
    def comportamiento_general(self):
        self.mover_hacia_jugador()
        self.intentar_disparar()

    # Movimiento hacia la posición actual del jugador
    def mover_hacia_jugador(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)  # Se asegura de evitar división entre cero
        self.rect.x += int(self.velocidad * dx / dist)
        self.rect.y += int(self.velocidad * dy / dist)

    # Verifica si ha pasado suficiente tiempo para permitir un nuevo disparo
    def intentar_disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_disparo > 2000:  # 2 segundos entre disparos
            self.disparar()
            self.tiempo_ultimo_disparo = ahora

    # Crea una bala dirigida hacia el jugador
    def disparar(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        angulo = math.atan2(dy, dx)  # Calcula el ángulo de disparo
        velocidad = 5
        vx = math.cos(angulo) * velocidad
        vy = math.sin(angulo) * velocidad

        # Crea una bala con dirección calculada y la agrega a los grupos de balas
        bala = Bullet(self.rect.centerx, self.rect.centery, vector=(vx, vy), image_path="assets/sprites/bullet_enemy.png")
        self.balas.add(bala)
        self.balas_global.add(bala)

    # Método de actualización que ejecuta el árbol de comportamiento y actualiza sus balas
    def update(self):
        self.arbol.ejecutar()
        self.balas.update()

    # Dibuja el enemigo y sus balas en pantalla
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.balas.draw(surface)
