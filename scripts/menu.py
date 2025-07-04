# menu.py - Menú principal del juego
import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Iniciar Juego", "Salir"]
        self.selected_index = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, 250 + i * 60))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def run(self):
        while True:
            self.draw()
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
                        if self.selected_index == 0:
                            return "start"
                        elif self.selected_index == 1:
                            pygame.quit()
                            sys.exit()
            self.clock.tick(60)
