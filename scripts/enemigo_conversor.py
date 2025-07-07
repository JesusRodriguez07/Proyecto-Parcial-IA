# scripts/enemigo_conversor.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
from scripts.a_estrella import a_estrella  # Importa el algoritmo A* para navegación
from scripts.arbol_comportamiento import Selector, Secuencia, Condicion, Accion  # Árbol de Comportamiento
from scripts.enemigo import Enemigo  # Hereda de la clase Enemigo base

# Clase que define un enemigo avanzado que puede convertir humanos en enemigos
class EnemigoConversor(Enemigo):
    sprite_converter = None  # Sprite compartido para todos los conversores

    def __init__(self, x, y, jugador, mapa, humanos, grupo_enemigos):
        # Llama al constructor de la clase base Enemigo
        super().__init__(x, y, jugador, mapa, humanos)

        self.grupo_enemigos = grupo_enemigos  # Referencia al grupo donde se agregarán nuevos enemigos

        # Carga la imagen del enemigo conversor solo una vez (patrón singleton de imagen)
        if EnemigoConversor.sprite_converter is None:
            EnemigoConversor.sprite_converter = pygame.image.load("assets/sprites/enemy_converter.png").convert_alpha()

        # Asigna la imagen y establece su posición
        self.image = EnemigoConversor.sprite_converter
        self.rect = self.image.get_rect(center=(x, y))

    # Método que se ejecuta cada frame del juego
    def update(self):
        super().update()  # Ejecuta la lógica de movimiento del Enemigo base

        # Verifica colisiones con humanos
        if self.humanos:
            colisiones = pygame.sprite.spritecollide(self, self.humanos, dokill=True)
            for humano in colisiones:
                # Si colisiona con un humano, lo convierte en un nuevo enemigo
                nuevo_enemigo = Enemigo(
                    humano.rect.centerx,
                    humano.rect.centery,
                    self.jugador,
                    self.mapa,
                    self.humanos
                )
                nuevo_enemigo.velocidad = self.velocidad  # El nuevo enemigo hereda la velocidad
                self.grupo_enemigos.add(nuevo_enemigo)  # Se agrega al grupo de enemigos activos
