import pygame
import random
from scripts.jugador import Jugador
from scripts.bala import Bullet
from scripts.menu import Menu
from scripts.pause_menu import PauseMenu
from scripts.enemigo import Enemigo
from scripts.explosion import Explosion

def mostrar_nivel(screen, nivel):
    font = pygame.font.Font(None, 64)
    texto = font.render(f"Nivel {nivel}", True, (255, 255, 0))
    rect = texto.get_rect(center=(400, 300))
    screen.fill((0, 0, 0))
    screen.blit(texto, rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron IA - Examen Final")
    clock = pygame.time.Clock()

    # 🎮 Gamepad setup
    pygame.joystick.init()
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Gamepad detectado: {joystick.get_name()}")

    menu = Menu(screen, joystick)
    action = menu.run()

    if action != "start":
        return

    # ▶️ Entra al juego
    nivel = 1
    jugador = Jugador(400, 300)
    bullets = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    explosiones = pygame.sprite.Group()
    mapa_vacio = [[0 for _ in range(25)] for _ in range(20)]
    pausa = PauseMenu(screen, joystick)

    enemigos_por_nivel = 6
    velocidad_base = 2
    mostrar_nivel(screen, nivel)

    tiempo_ultimo_spawn = pygame.time.get_ticks()
    enemigos_generados = 0
    paused = False
    running = True

    while running:
        clock.tick(60)
        ahora = pygame.time.get_ticks()

        dx = dy = 0
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 9:
                paused = True

        if paused:
            opcion = pausa.run()
            if opcion == "resume":
                paused = False
                continue
            elif opcion == "menu":
                main()
                return
            elif opcion == "exit":
                running = False
                break

        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            if abs(axis_x) > 0.3: dx = int(axis_x / abs(axis_x))
            if abs(axis_y) > 0.3: dy = int(axis_y / abs(axis_y))

        jugador.update(keys, dx, dy, bullets, joystick)

        for i, enemigo in enumerate(enemigos):
            if ahora % 2 == i % 2:
                enemigo.update()

        bullets.update()
        explosiones.update()

        if enemigos_generados < enemigos_por_nivel:
            if ahora - tiempo_ultimo_spawn > 600:
                while True:
                    ex = random.randint(50, 750)
                    ey = random.randint(50, 550)
                    if abs(ex - jugador.rect.centerx) > 100 and abs(ey - jugador.rect.centery) > 100:
                        break
                enemigo = Enemigo(ex, ey, jugador, mapa_vacio)
                enemigo.velocidad = velocidad_base + (nivel * 0.5)
                enemigos.add(enemigo)
                enemigos_generados += 1
                tiempo_ultimo_spawn = ahora

        for bullet in bullets:
            impactos = pygame.sprite.spritecollide(bullet, enemigos, dokill=True)
            for enemigo in impactos:
                explosiones.add(Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                bullet.kill()

        screen.fill((0, 0, 0))
        screen.blit(jugador.image, jugador.rect)
        bullets.draw(screen)
        for enemigo in enemigos:
            if screen.get_rect().colliderect(enemigo.rect):
                screen.blit(enemigo.image, enemigo.rect)
        explosiones.draw(screen)

        pygame.display.flip()

        # ✅ Check: avanzar de nivel
        if enemigos_generados == enemigos_por_nivel and len(enemigos) == 0:
            nivel += 1
            enemigos_por_nivel += 4
            velocidad_base += 0.2
            mostrar_nivel(screen, nivel)
            enemigos_generados = 0
            tiempo_ultimo_spawn = pygame.time.get_ticks()

if __name__ == "__main__":
    main()
