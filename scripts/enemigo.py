# scripts/enemigo.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
from scripts.a_estrella import a_estrella  # Algoritmo de búsqueda A*
from scripts.arbol_comportamiento import Selector, Secuencia, Condicion, Accion  # Componentes del árbol de comportamiento

# Clase Enemigo: enemigo básico con IA basada en árbol de comportamiento
class Enemigo(pygame.sprite.Sprite):
    enemy_sprite = None  # Caché para no recargar el sprite varias veces

    def __init__(self, x, y, jugador, mapa, grupo_humanos=None):
        super().__init__()

        # Carga la imagen del enemigo si aún no está cargada
        if Enemigo.enemy_sprite is None:
            Enemigo.enemy_sprite = pygame.image.load("assets/sprites/enemy.png").convert_alpha()

        self.image = Enemigo.enemy_sprite
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial

        self.jugador = jugador  # Referencia al jugador
        self.humanos = grupo_humanos  # Grupo de humanos a los que puede atacar o convertir
        self.velocidad = 2
        self.mapa = mapa  # Mapa en forma de matriz
        self.grid_size = 24  # Tamaño de cada celda del mapa (para A*)
        self.camino = []  # Ruta generada por A*
        self.tiempo_ruta = 0  # Tiempo en que se calculó la última ruta
        self.objetivo_actual = None  # Última posición objetivo
        self.objetivo_secundario = None  # Humano más cercano (si lo hay)

        # Árbol de comportamiento del enemigo
        self.arbol = Selector([
            # Si el jugador está cerca, lo persigue directamente
            Secuencia([
                Condicion(self.jugador_cerca),
                Accion(self.mover_directo_jugador)
            ]),
            # Si un humano está cerca, lo persigue
            Secuencia([
                Condicion(self.humano_cerca),
                Accion(self.perseguir_humano)
            ]),
            # Si no, busca al jugador usando A*
            Accion(self.buscar_con_a_estrella)
        ])

    # Verifica si el jugador está dentro de un rango de 150 píxeles
    def jugador_cerca(self):
        distancia = self.rect.centerx - self.jugador.rect.centerx, self.rect.centery - self.jugador.rect.centery
        return abs(distancia[0]) < 150 and abs(distancia[1]) < 150

    # Busca al humano más cercano dentro de un radio de 120 píxeles
    def humano_cerca(self):
        if not self.humanos:
            return False

        cercano = None
        distancia_min = float("inf")

        for humano in self.humanos:
            dx = humano.rect.centerx - self.rect.centerx
            dy = humano.rect.centery - self.rect.centery
            distancia = (dx**2 + dy**2)**0.5

            if distancia < 120 and distancia < distancia_min:
                distancia_min = distancia
                cercano = humano

        self.objetivo_secundario = cercano
        return cercano is not None

    # Movimiento directo hacia el jugador (sin pathfinding)
    def mover_directo_jugador(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)

        self.rect.x += int(self.velocidad * dx / dist)
        self.rect.y += int(self.velocidad * dy / dist)

    # Movimiento directo hacia el humano más cercano
    def perseguir_humano(self):
        if not self.objetivo_secundario:
            return

        dx = self.objetivo_secundario.rect.centerx - self.rect.centerx
        dy = self.objetivo_secundario.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2)**0.5)

        self.rect.x += int(self.velocidad * dx / dist)
        self.rect.y += int(self.velocidad * dy / dist)

    # Usa el algoritmo A* para generar una ruta hacia el jugador
    def buscar_con_a_estrella(self):
        now = pygame.time.get_ticks()
        jugador_pos = (self.jugador.rect.centerx // self.grid_size,
                       self.jugador.rect.centery // self.grid_size)

        # Si el jugador se movió o pasaron 5 segundos, recalcula ruta
        if (self.objetivo_actual != jugador_pos) or (now - self.tiempo_ruta > 5000):
            inicio = (self.rect.centerx // self.grid_size, self.rect.centery // self.grid_size)
            objetivo = jugador_pos
            ruta = a_estrella(self.mapa, inicio, objetivo)

            # Si se encontró ruta válida, la guarda
            if ruta and len(ruta) > 1:
                self.camino = ruta[1:]
            else:
                self.camino = [(objetivo[0], objetivo[1])]

            self.objetivo_actual = objetivo
            self.tiempo_ruta = now

        # Sigue el camino generado paso a paso
        if self.camino:
            siguiente = self.camino[0]
            target_px = (
                siguiente[0] * self.grid_size + self.grid_size // 2,
                siguiente[1] * self.grid_size + self.grid_size // 2
            )

            dx = target_px[0] - self.rect.centerx
            dy = target_px[1] - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)

            self.rect.x += int(self.velocidad * dx / dist)
            self.rect.y += int(self.velocidad * dy / dist)

            # Si llegó al punto actual de la ruta, lo elimina de la lista
            if abs(dx) < 5 and abs(dy) < 5:
                self.camino.pop(0)

    # Método principal que se llama en cada frame para ejecutar el árbol de comportamiento
    def update(self):
        self.arbol.ejecutar()
