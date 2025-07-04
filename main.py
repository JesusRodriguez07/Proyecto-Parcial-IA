# main.py - Entrada principal del juego
import pygame
from scripts.menu import Menu
from scripts.jugador import Jugador

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron 2084 - Examen IA")

    # Mostrar el menú
    menu = Menu(screen)
    action = menu.run()

    if action == "start":
        jugador = Jugador(400, 300)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(jugador)

        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill((30, 30, 30))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            all_sprites.update(keys)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
