import pygame
import sys

# Clase PauseMenu: muestra un menú cuando el juego está pausado
# Autor: jesus rodriguez - 12-sisn-2-043
class PauseMenu:
    def __init__(self, screen, joystick):
        self.screen = screen              # Pantalla donde se dibuja
        self.joystick = joystick          # Joystick (si está conectado)
        self.options = ["Reanudar", "Menú principal", "Salir"]  # Opciones disponibles
        self.selected = 0                # Índice de la opción actual seleccionada
        self.font = pygame.font.Font(None, 60)  # Fuente para mostrar texto
        self.hat_cooldown = 0            # Temporizador para evitar repeticiones con el D-pad
        self.axis_cooldown = 0           # Temporizador para el stick analógico

    # Dibuja el menú de pausa en pantalla
    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro
        title = self.font.render("PAUSA", True, (255, 255, 255))  # Título principal

        # Centrar el título
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        # Dibuja las opciones
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            text = self.font.render(option, True, color)
            x = self.screen.get_width() // 2 - text.get_width() // 2
            y = 200 + i * 70
            self.screen.blit(text, (x, y))

        pygame.display.flip()  # Actualiza la pantalla

    # Ejecuta el bucle del menú de pausa y retorna la opción seleccionada
    def run(self):
        clock = pygame.time.Clock()
        self.hat_cooldown = 0
        self.axis_cooldown = 0

        while True:
            clock.tick(60)  # Limita a 60 FPS
            self.draw()     # Dibuja el menú cada frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Navegación por teclado
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.resolve_option()  # Ejecuta la opción seleccionada

                # Confirmación con botón del joystick
                elif event.type == pygame.JOYBUTTONDOWN and self.joystick:
                    if event.button == 1:  # Botón A / Cruz
                        return self.resolve_option()
                    elif event.button == 9:  # Botón START
                        return self.resolve_option()

            # Navegación con D-pad del joystick
            if self.joystick and self.joystick.get_numhats() > 0:
                hat = self.joystick.get_hat(0)
                if self.hat_cooldown == 0:
                    if hat[1] == 1:  # Arriba
                        self.selected = (self.selected - 1) % len(self.options)
                        self.hat_cooldown = 6
                    elif hat[1] == -1:  # Abajo
                        self.selected = (self.selected + 1) % len(self.options)
                        self.hat_cooldown = 6
                elif hat[1] == 0:
                    self.hat_cooldown = max(0, self.hat_cooldown - 1)

            # Navegación con el stick analógico del joystick
            if self.joystick:
                axis_y = self.joystick.get_axis(1)
                if self.axis_cooldown == 0:
                    if axis_y < -0.5:  # Mover arriba
                        self.selected = (self.selected - 1) % len(self.options)
                        self.axis_cooldown = 6
                    elif axis_y > 0.5:  # Mover abajo
                        self.selected = (self.selected + 1) % len(self.options)
                        self.axis_cooldown = 6
                elif abs(axis_y) < 0.3:
                    self.axis_cooldown = max(0, self.axis_cooldown - 1)

    # Resuelve la opción seleccionada y devuelve un valor para el main
    def resolve_option(self):
        if self.selected == 0:
            return "resume"         # Reanudar juego
        elif self.selected == 1:
            return "menu"           # Volver al menú principal
        elif self.selected == 2:
            return "exit"           # Salir del juego
