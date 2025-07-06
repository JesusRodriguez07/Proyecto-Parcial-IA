# main.py actualizado con disparadores usando grupo global de balas
# Autor: jesus rodriguez - 12-sisn-2-043

import pygame
import random
from scripts.jugador import Jugador
from scripts.bala import Bullet
from scripts.menu import Menu
from scripts.pause_menu import PauseMenu
from scripts.enemigo import Enemigo
from scripts.enemigo_disparo import EnemigoDisparo
from scripts.explosion import Explosion
from scripts.humano import Humano

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

    nivel = 1
    jugador = Jugador(400, 300)
    bullets = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    disparadores = pygame.sprite.Group()
    balas_enemigas = pygame.sprite.Group()
    explosiones = pygame.sprite.Group()
    humanos = pygame.sprite.Group()
    mapa_vacio = [[0 for _ in range(25)] for _ in range(20)]
    pausa = PauseMenu(screen, joystick)

    enemigos_por_nivel = 6
    velocidad_base = 2
    puntaje = 0

    mostrar_nivel(screen, nivel)

    for _ in range(random.randint(3, 5)):
        while True:
            hx = random.randint(50, 750)
            hy = random.randint(50, 550)
            if abs(hx - jugador.rect.centerx) > 80 and abs(hy - jugador.rect.centery) > 80:
                break
        humano = Humano(hx, hy)
        humanos.add(humano)

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

        for disparador in disparadores:
            disparador.update()

        bullets.update()
        balas_enemigas.update()
        explosiones.update()
        humanos.update()

        rescatados = pygame.sprite.spritecollide(jugador, humanos, dokill=True)
        puntaje += 1000 * len(rescatados)

        for enemigo in enemigos:
            pygame.sprite.spritecollide(enemigo, humanos, dokill=True)

        for disparador in disparadores:
            pygame.sprite.spritecollide(disparador, humanos, dokill=True)

        if enemigos_generados < enemigos_por_nivel:
            if ahora - tiempo_ultimo_spawn > 600:
                while True:
                    ex = random.randint(50, 750)
                    ey = random.randint(50, 550)
                    if abs(ex - jugador.rect.centerx) > 100 and abs(ey - jugador.rect.centery) > 100:
                        break

                if nivel >= 2 and random.random() < min(0.2 + nivel * 0.05, 0.5):
                    enemigo = EnemigoDisparo(ex, ey, jugador, balas_enemigas)
                    disparadores.add(enemigo)
                else:
                    enemigo = Enemigo(ex, ey, jugador, mapa_vacio, humanos)
                    enemigo.velocidad = velocidad_base + (nivel * 0.5)
                    enemigos.add(enemigo)

                enemigos_generados += 1
                tiempo_ultimo_spawn = ahora

        for bullet in bullets:
            impactos = pygame.sprite.spritecollide(bullet, enemigos, dokill=True)
            for enemigo in impactos:
                explosiones.add(Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                bullet.kill()

            impactos2 = pygame.sprite.spritecollide(bullet, disparadores, dokill=True)
            for enemigo in impactos2:
                explosiones.add(Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                bullet.kill()

        screen.fill((0, 0, 0))
        screen.blit(jugador.image, jugador.rect)
        humanos.draw(screen)
        bullets.draw(screen)
        balas_enemigas.draw(screen)

        for enemigo in enemigos:
            if screen.get_rect().colliderect(enemigo.rect):
                screen.blit(enemigo.image, enemigo.rect)

        for disparador in disparadores:
            if screen.get_rect().colliderect(disparador.rect):
                disparador.draw(screen)

        explosiones.draw(screen)

        font = pygame.font.Font(None, 36)
        texto_puntos = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        screen.blit(texto_puntos, (10, 10))

        pygame.display.flip()

        if enemigos_generados == enemigos_por_nivel and len(enemigos) + len(disparadores) == 0:
            nivel += 1
            enemigos_por_nivel += 4
            velocidad_base += 0.2
            mostrar_nivel(screen, nivel)
            enemigos_generados = 0
            tiempo_ultimo_spawn = pygame.time.get_ticks()

            humanos.empty()
            for _ in range(random.randint(3, 5)):
                while True:
                    hx = random.randint(50, 750)
                    hy = random.randint(50, 550)
                    if abs(hx - jugador.rect.centerx) > 80 and abs(hy - jugador.rect.centery) > 80:
                        break
                humano = Humano(hx, hy)
                humanos.add(humano)

if __name__ == "__main__":
    main()
