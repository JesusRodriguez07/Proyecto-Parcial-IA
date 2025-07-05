import pygame
from scripts.bala import Bullet

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Cargar la hoja de sprites desde assets/sprites/player.png
        sprite_sheet = pygame.image.load("assets/sprites/player.png").convert_alpha()

        # Cada sprite mide 16x16 y están alineados horizontalmente
        self.sprites = {
        'up': sprite_sheet.subsurface((0, 0, 24, 24)),
        'down': sprite_sheet.subsurface((24, 0, 24, 24)),
        'left': sprite_sheet.subsurface((48, 0, 24, 24)),
        'right': sprite_sheet.subsurface((72, 0, 24, 24)),
}


        self.direction = "down"
        self.image = self.sprites[self.direction]  # sin escalar
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.last_shot = 0
        self.shot_delay = 200  # milisegundos

    def update(self, keys, dx, dy, bullets_group, joystick):
        # Cambiar dirección según el movimiento
        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"

        # Actualizar sprite y posición
        self.image = self.sprites[self.direction]  # sin escala
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Disparo con stick derecho
        now = pygame.time.get_ticks()
        if joystick:
            joy_dx = joystick.get_axis(2)
            joy_dy = joystick.get_axis(3)
            threshold = 0.4
            direction = None

            if joy_dx < -threshold:
                direction = "left"
            elif joy_dx > threshold:
                direction = "right"
            elif joy_dy < -threshold:
                direction = "up"
            elif joy_dy > threshold:
                direction = "down"

            if direction and now - self.last_shot > self.shot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
                bullets_group.add(bullet)
                self.last_shot = now







