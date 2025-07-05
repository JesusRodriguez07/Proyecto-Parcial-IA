# pause_menu.py - Menú de pausa dentro del juego
import pygame
import sys
import time

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Reanudar", "Salir al Menú Principal"]
        self.selected_index = 0
        self.last_move_time = 0

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, 250 + i * 60))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def run(self, joystick=None):
        while True:
            self.draw()
            now = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return "resume" if self.selected_index == 0 else "menu"

            if joystick:
                hat = (0, 0)
                if joystick.get_numhats() > 0:
                    hat = joystick.get_hat(0)

                if hat[1] == 1 and now - self.last_move_time > 0.3:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.last_move_time = now
                elif hat[1] == -1 and now - self.last_move_time > 0.3:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.last_move_time = now

                axis_y = joystick.get_axis(1)
                if axis_y < -0.5 and now - self.last_move_time > 0.3:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.last_move_time = now
                elif axis_y > 0.5 and now - self.last_move_time > 0.3:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.last_move_time = now

                if joystick.get_button(1):
                    return "resume" if self.selected_index == 0 else "menu"

            self.clock.tick(30)
