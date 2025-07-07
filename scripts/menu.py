import pygame
import sys

# Clase Menu: muestra el menú inicial del juego con control por teclado o joystick
class Menu:
    def __init__(self, screen, joystick=None):
        self.screen = screen  # Superficie donde se dibuja el menú
        self.joystick = joystick  # Joystick (si está conectado)
        self.options = ["Iniciar juego", "Salir"]  # Opciones disponibles en el menú
        self.selected = 0  # Índice de la opción seleccionada
        self.font = pygame.font.Font(None, 60)  # Fuente del texto
        self.hat_cooldown = 0  # Temporizador para evitar cambio continuo con D-pad
        self.axis_cooldown = 0  # Temporizador para el stick analógico

    # Dibuja el menú en pantalla
    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro
        title = self.font.render("Robotron 2084", True, (255, 255, 255))  # Título

        # Centrar el título en la parte superior
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        # Dibuja cada opción del menú
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            text = self.font.render(option, True, color)
            x = self.screen.get_width() // 2 - text.get_width() // 2
            y = 200 + i * 70
            self.screen.blit(text, (x, y))

        pygame.display.flip()  # Refresca la pantalla

    # Ejecuta el bucle del menú y retorna la opción elegida
    def run(self):
        clock = pygame.time.Clock()
        self.hat_cooldown = 0
        self.axis_cooldown = 0

        while True:
            self.draw()  # Dibuja el menú en cada frame

            # Manejo del D-Pad del gamepad
            if self.joystick and self.joystick.get_numhats() > 0:
                hat = self.joystick.get_hat(0)
                if self.hat_cooldown == 0:
                    if hat[1] == 1:  # D-pad arriba
                        self.selected = (self.selected - 1) % len(self.options)
                        self.hat_cooldown = 6
                    elif hat[1] == -1:  # D-pad abajo
                        self.selected = (self.selected + 1) % len(self.options)
                        self.hat_cooldown = 6
                elif hat[1] == 0:
                    self.hat_cooldown = max(0, self.hat_cooldown - 1)

            # Manejo del stick analógico vertical
            if self.joystick:
                axis_y = self.joystick.get_axis(1)
                if self.axis_cooldown == 0:
                    if axis_y < -0.6:  # Hacia arriba
                        self.selected = (self.selected - 1) % len(self.options)
                        self.axis_cooldown = 6
                    elif axis_y > 0.6:  # Hacia abajo
                        self.selected = (self.selected + 1) % len(self.options)
                        self.axis_cooldown = 6
                elif abs(axis_y) < 0.3:
                    self.axis_cooldown = max(0, self.axis_cooldown - 1)

            # Manejo de eventos del sistema
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Teclado: navegación y selección
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return "start" if self.selected == 0 else "exit"

                # Botones del gamepad (botón 0 o 1 = confirmar)
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in [0, 1]:
                        return "start" if self.selected == 0 else "exit"

            clock.tick(60)  # 60 FPS

