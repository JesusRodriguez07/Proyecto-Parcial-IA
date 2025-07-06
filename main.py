import pygame
from scripts.jugador import Jugador
from scripts.bala import Bullet
from scripts.menu import Menu
from scripts.pause_menu import PauseMenu
from scripts.enemigo import Enemigo
from scripts.explosion import Explosion

def crear_mapa_dummy():
    return [[0 for _ in range(25)] for _ in range(20)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron 2084 - Examen IA")
    clock = pygame.time.Clock()

    pygame.joystick.init()
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Gamepad detectado: {joystick.get_name()}")

    menu = Menu(screen, joystick)
    action = menu.run()

    if action == "start":
        jugador = Jugador(400, 300)
        bullets = pygame.sprite.Group()
        enemigos = pygame.sprite.Group()
        explosiones = pygame.sprite.Group()

        mapa = crear_mapa_dummy()

        for i in range(3):
            enemigo = Enemigo(100 + i * 60, 100, jugador, mapa)
            enemigos.add(enemigo)

        pause_menu = PauseMenu(screen, joystick)
        paused = False
        running = True

        while running:
            screen.fill((0, 0, 0))  # fondo negro

            keys = pygame.key.get_pressed()
            dx = dy = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = True
                if event.type == pygame.JOYBUTTONDOWN and event.button == 9:
                    paused = True

            if paused:
                paused = False
                pause_action = pause_menu.run()
                if pause_action == "resume":
                    continue
                elif pause_action == "menu":
                    main()
                    return
                elif pause_action == "quit":
                    running = False
                    break

            if keys[pygame.K_LEFT]: dx = -1
            if keys[pygame.K_RIGHT]: dx = 1
            if keys[pygame.K_UP]: dy = -1
            if keys[pygame.K_DOWN]: dy = 1

            if joystick:
                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)
                threshold = 0.3
                if abs(axis_x) > threshold:
                    dx = int(axis_x / abs(axis_x))
                if abs(axis_y) > threshold:
                    dy = int(axis_y / abs(axis_y))

            jugador.update(keys, dx, dy, bullets, joystick)
            bullets.update()
            enemigos.update()
            explosiones.update()

            # Colisiones: balas vs enemigos
            for bala in bullets:
                impactados = pygame.sprite.spritecollide(bala, enemigos, True)
                if impactados:
                    bala.kill()
                    for enemigo in impactados:
                        explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery)
                        explosiones.add(explosion)

            screen.blit(jugador.image, jugador.rect)
            bullets.draw(screen)
            enemigos.draw(screen)
            explosiones.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

