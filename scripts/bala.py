# scripts/bala.py
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame  # Importamos la librería pygame para trabajar con gráficos y sprites

# Clase Bullet que representa una bala, heredando de Sprite de Pygame
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=None, vector=None, image_path=None):
        super().__init__()  # Inicializa el objeto como un Sprite

        # Si no se especifica una imagen, se carga una por defecto
        if image_path is None:
            image_path = "assets/images/bullet.png"

        # Carga la imagen de la bala con canal alfa (transparencia)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial de la bala

        self.speed = 10  # Velocidad fija de la bala
        self.direction = direction  # Dirección textual (arriba, abajo, etc.)
        self.vector = vector        # Vector de dirección (vx, vy) usado por enemigos

    # Método que se ejecuta en cada frame del juego para actualizar la posición de la bala
    def update(self):
        if self.vector:
            # Si la bala se mueve por vector (usada por enemigos), se actualiza con las componentes
            self.rect.x += self.vector[0]
            self.rect.y += self.vector[1]
        elif self.direction:
            # Si tiene dirección textual, mueve según esa dirección
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

        # Si la bala sale de la pantalla (800x600), se elimina del juego
        if (self.rect.bottom < 0 or self.rect.top > 600 or
            self.rect.right < 0 or self.rect.left > 800):
            self.kill()
