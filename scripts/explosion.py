import pygame

# Clase Explosion: representa una animación breve cuando un enemigo es destruido
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Inicializa como un sprite

        # Carga la imagen de explosión desde archivo y le aplica transparencia (canal alfa)
        self.image = pygame.image.load("assets/sprites/explosion.png").convert_alpha()

        # Redimensiona la imagen a 32x32 píxeles para que no ocupe demasiado espacio
        self.image = pygame.transform.scale(self.image, (32, 32))

        # Establece la posición de la explosión centrada en (x, y)
        self.rect = self.image.get_rect(center=(x, y))

        # Duración de la explosión en frames. Después de esto se elimina
        self.timer = 10  # Dura aproximadamente 1/6 de segundo a 60 FPS

    # Método que se ejecuta en cada frame
    def update(self):
        self.timer -= 1  # Disminuye el contador
        if self.timer <= 0:
            self.kill()  # Elimina la explosión del grupo de sprites
