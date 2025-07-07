import pygame
import sys

class PauseMenu:
    def __init__(self, screen, joystick):
        self.screen = screen
        self.joystick = joystick
        self.options = ["Reanudar", "Menú principal", "Salir"]
        self.selected = 0
        self.font = pygame.font.Font(None, 60)
        self.hat_cooldown = 0
        self.axis_cooldown = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("PAUSA", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            text = self.font.render(option, True, color)
            x = self.screen.get_width() // 2 - text.get_width() // 2
            y = 200 + i * 70
            self.screen.blit(text, (x, y))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        self.hat_cooldown = 0
        self.axis_cooldown = 0

        while True:
            clock.tick(60)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.resolve_option()

                elif event.type == pygame.JOYBUTTONDOWN and self.joystick:
                    if event.button == 1:  # Botón A / Cruz
                        return self.resolve_option()
                    elif event.button == 9:  # Botón START también confirma
                        return self.resolve_option()

            # Entrada del D-pad (hat)
            if self.joystick and self.joystick.get_numhats() > 0:
                hat = self.joystick.get_hat(0)
                if self.hat_cooldown == 0:
                    if hat[1] == 1:
                        self.selected = (self.selected - 1) % len(self.options)
                        self.hat_cooldown = 6
                    elif hat[1] == -1:
                        self.selected = (self.selected + 1) % len(self.options)
                        self.hat_cooldown = 6
                elif hat[1] == 0:
                    self.hat_cooldown = max(0, self.hat_cooldown - 1)

            # Entrada de stick analógico (eje Y)
            if self.joystick:
                axis_y = self.joystick.get_axis(1)
                if self.axis_cooldown == 0:
                    if axis_y < -0.5:
                        self.selected = (self.selected - 1) % len(self.options)
                        self.axis_cooldown = 6
                    elif axis_y > 0.5:
                        self.selected = (self.selected + 1) % len(self.options)
                        self.axis_cooldown = 6
                elif abs(axis_y) < 0.3:
                    self.axis_cooldown = max(0, self.axis_cooldown - 1)

    def resolve_option(self):
        if self.selected == 0:
            return "resume"
        elif self.selected == 1:
            return "menu"
        elif self.selected == 2:
            return "exit"
