# main.py - Entrada principal del juego
import pygame
from scripts.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron 2084 - Examen IA")

    # Mostrar el menú
    menu = Menu(screen)
    action = menu.run()

    if action == "start":
        # Aquí arrancaría el bucle del juego 
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Aquí iría la lógica del juego (jugador, enemigos, IA, etc.)
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
