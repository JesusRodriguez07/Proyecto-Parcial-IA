import pygame
from scripts.menu import Menu
from scripts.jugador import Jugador
from scripts.pause_menu import PauseMenu

def menu_loop(screen, joystick):
    menu = Menu(screen, joystick)
    return menu.run()

def game_loop(screen, joystick):
    jugador = Jugador(400, 300)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jugador)

    pause_menu = PauseMenu(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()

        dx = joystick.get_axis(0) if joystick else 0
        dy = joystick.get_axis(1) if joystick else 0

        if joystick and joystick.get_numhats() > 0:
            hat_x, hat_y = joystick.get_hat(0)
            dx += hat_x
            dy += -hat_y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # Menú de pausa
        if joystick and joystick.get_button(9):
            pause = PauseMenu(screen)
            choice = pause.run(joystick)
            if choice == "menu":
                return "menu"

        all_sprites.update(keys, dx, dy)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron 2084 - Examen IA")

    pygame.joystick.init()
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Gamepad detectado: {joystick.get_name()}")
    else:
        print("⚠️ No se detectó ningún Gamepad")

    while True:
        action = menu_loop(screen, joystick)
        if action == "start":
            result = game_loop(screen, joystick)
            if result == "quit":
                break
        elif action == "quit":
            break

    pygame.quit()

if __name__ == '__main__':
    main()
