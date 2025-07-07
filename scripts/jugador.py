import pygame
from scripts.bala import Bullet  # Importa la clase Bullet para disparar proyectiles
# Autor: jesus rodriguez - 12-sisn-2-043

# Clase Jugador: controla al personaje principal del juego
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Carga la hoja de sprites del jugador
        sprite_sheet = pygame.image.load("assets/sprites/player.png").convert_alpha()

        # Recorta la hoja en 4 direcciones (cada sprite de 24x24 px)
        self.sprites = {
            'up': sprite_sheet.subsurface((0, 0, 24, 24)),
            'down': sprite_sheet.subsurface((24, 0, 24, 24)),
            'left': sprite_sheet.subsurface((48, 0, 24, 24)),
            'right': sprite_sheet.subsurface((72, 0, 24, 24)),
        }

        self.direction = "down"  # Dirección inicial del jugador
        self.image = self.sprites[self.direction]  # Imagen que se mostrará
        self.rect = self.image.get_rect(center=(x, y))  # Posición inicial

        self.speed = 5  # Velocidad de movimiento
        self.last_shot = 0  # Tiempo del último disparo
        self.shot_delay = 200  # Tiempo mínimo entre disparos (en milisegundos)
        self.disparo_realizado = False  # Señal para activar sonido en el main

    # Método principal del jugador que se llama cada frame
    def update(self, keys, dx, dy, bullets_group, joystick):
        self.disparo_realizado = False  # Se reinicia al inicio del frame

        # Ignorar movimientos muy pequeños (ruido del stick o joystick)
        if abs(dx) < 0.1: dx = 0
        if abs(dy) < 0.1: dy = 0

        # Determina la dirección mirando qué componente (x o y) predomina
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        elif abs(dy) > 0:
            self.direction = "down" if dy > 0 else "up"

        # Cambia el sprite según dirección
        self.image = self.sprites[self.direction]

        # Mueve al jugador
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

        # Limita al jugador dentro de los bordes de la pantalla (800x600)
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

        # Lógica para disparar con el stick derecho del joystick
        now = pygame.time.get_ticks()
        if joystick:
            joy_dx = joystick.get_axis(2)  # Eje horizontal del stick derecho
            joy_dy = joystick.get_axis(3)  # Eje vertical del stick derecho
            threshold = 0.4  # Sensibilidad mínima para detectar dirección
            direction = None

            # Determina hacia dónde disparar según el stick
            if joy_dx < -threshold: direction = "left"
            elif joy_dx > threshold: direction = "right"
            elif joy_dy < -threshold: direction = "up"
            elif joy_dy > threshold: direction = "down"

            # Si hay una dirección válida y ya pasó suficiente tiempo desde el último disparo
            if direction and now - self.last_shot > self.shot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.centery, direction)  # Crea bala
                bullets_group.add(bullet)  # La agrega al grupo de balas
                self.last_shot = now
                self.disparo_realizado = True  # Activa sonido de disparo en el main
