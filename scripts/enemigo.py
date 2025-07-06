import pygame
from scripts.a_estrella import a_estrella
from scripts.arbol_comportamiento import Selector, Secuencia, Condicion, Accion

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, jugador, mapa):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.jugador = jugador
        self.velocidad = 2
        self.mapa = mapa
        self.grid_size = 24
        self.camino = []
        self.tiempo_ruta = 0

        self.arbol = Selector([
            Secuencia([
                Condicion(self.jugador_cerca),
                Accion(self.mover_directo)
            ]),
            Accion(self.buscar_con_a_estrella)
        ])

    def jugador_cerca(self):
        distancia = self.rect.centerx - self.jugador.rect.centerx, self.rect.centery - self.jugador.rect.centery
        return abs(distancia[0]) < 150 and abs(distancia[1]) < 150

    def mover_directo(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.rect.x += int(self.velocidad * dx / dist)
        self.rect.y += int(self.velocidad * dy / dist)

    def buscar_con_a_estrella(self):
        now = pygame.time.get_ticks()
        if not self.camino or now - self.tiempo_ruta > 1000:
            inicio = (self.rect.centerx // self.grid_size, self.rect.centery // self.grid_size)
            objetivo = (self.jugador.rect.centerx // self.grid_size, self.jugador.rect.centery // self.grid_size)
            ruta = a_estrella(self.mapa, inicio, objetivo)
            self.camino = ruta[1:] if ruta else []
            self.tiempo_ruta = now

        if self.camino:
            siguiente = self.camino[0]
            target_px = (siguiente[0] * self.grid_size + self.grid_size // 2,
                         siguiente[1] * self.grid_size + self.grid_size // 2)

            dx = target_px[0] - self.rect.centerx
            dy = target_px[1] - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)

            self.rect.x += int(self.velocidad * dx / dist)
            self.rect.y += int(self.velocidad * dy / dist)

            if abs(dx) < 5 and abs(dy) < 5:
                self.camino.pop(0)

    def update(self):
        self.arbol.ejecutar()
