import pygame
from scripts.bala import Bullet

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        sprite_sheet = pygame.image.load("assets/sprites/player.png").convert_alpha()
        self.sprites = {
            'up': sprite_sheet.subsurface((0, 0, 24, 24)),
            'down': sprite_sheet.subsurface((24, 0, 24, 24)),
            'left': sprite_sheet.subsurface((48, 0, 24, 24)),
            'right': sprite_sheet.subsurface((72, 0, 24, 24)),
        }

        self.direction = "down"
        self.image = self.sprites[self.direction]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.last_shot = 0
        self.shot_delay = 200
        self.disparo_realizado = False  # ← Añadido para que el main reproduzca sonido

    def update(self, keys, dx, dy, bullets_group, joystick):
        self.disparo_realizado = False  # ← Se reinicia cada frame

        if abs(dx) < 0.1: dx = 0
        if abs(dy) < 0.1: dy = 0

        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        elif abs(dy) > 0:
            self.direction = "down" if dy > 0 else "up"

        self.image = self.sprites[self.direction]
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

        # Limitar dentro de pantalla
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

        # Disparo con stick derecho
        now = pygame.time.get_ticks()
        if joystick:
            joy_dx = joystick.get_axis(2)
            joy_dy = joystick.get_axis(3)
            threshold = 0.4
            direction = None

            if joy_dx < -threshold: direction = "left"
            elif joy_dx > threshold: direction = "right"
            elif joy_dy < -threshold: direction = "up"
            elif joy_dy > threshold: direction = "down"

            if direction and now - self.last_shot > self.shot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
                bullets_group.add(bullet)
                self.last_shot = now
                self.disparo_realizado = True  # ← ¡Señal para reproducir el sonido!
