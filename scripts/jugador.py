# jugador.py - Clase del jugador
import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 255))  # Verde
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidad = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.velocidad

        # Limitar dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
