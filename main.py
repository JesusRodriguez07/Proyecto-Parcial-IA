import pygame
import random
from scripts.jugador import Jugador
from scripts.bala import Bullet
from scripts.menu import Menu
from scripts.pause_menu import PauseMenu
from scripts.enemigo import Enemigo
from scripts.enemigo_disparo import EnemigoDisparo
from scripts.enemigo_conversor import EnemigoConversor
from scripts.explosion import Explosion
from scripts.humano import Humano

def mostrar_game_over(screen, puntaje, nivel, joystick=None):
    font = pygame.font.Font(None, 72)
    texto = font.render("GAME OVER", True, (255, 0, 0))
    texto2 = pygame.font.Font(None, 36).render("Presiona [R] para reiniciar o [ESC] para salir", True, (255, 255, 255))
    texto_puntaje = font.render(f"Puntaje: {puntaje}", True, (255, 255, 0))
    texto_nivel = font.render(f"Nivel: {nivel}", True, (255, 200, 0))
    rect = texto.get_rect(center=(400, 180))
    rect2 = texto2.get_rect(center=(400, 420))
    rect_puntaje = texto_puntaje.get_rect(center=(400, 250))
    rect_nivel = texto_nivel.get_rect(center=(400, 320))
    screen.fill((0, 0, 0))
    screen.blit(texto, rect)
    screen.blit(texto_puntaje, rect_puntaje)
    screen.blit(texto_nivel, rect_nivel)
    screen.blit(texto2, rect2)
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    esperando = False
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.JOYBUTTONDOWN and joystick:
                if event.button == 1:
                    esperando = False
                    main()
                elif event.button == 9:
                    esperando = False
                    main()

def mostrar_nivel(screen, nivel, vidas):
    font = pygame.font.Font(None, 64)
    texto = font.render(f"Nivel {nivel}", True, (255, 255, 0))
    texto_vidas = font.render(f"Vidas: {vidas}", True, (255, 100, 100))
    rect = texto.get_rect(center=(400, 260))
    rect_vidas = texto_vidas.get_rect(center=(400, 330))
    screen.fill((0, 0, 0))
    screen.blit(texto, rect)
    screen.blit(texto_vidas, rect_vidas)
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robotron IA - Examen Final")
    clock = pygame.time.Clock()

    pygame.mixer.init()

    # 🎵 Música de fondo
    pygame.mixer.music.load("assets/music/fondo.ogg")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # 🔊 Efectos
    sonido_disparo = pygame.mixer.Sound("assets/sounds/disparo.wav")
    sonido_explosion = pygame.mixer.Sound("assets/sounds/explosion.wav")
    sonido_golpe = pygame.mixer.Sound("assets/sounds/golpe.wav")
    sonido_rescate = pygame.mixer.Sound("assets/sounds/rescate.wav")

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
    vidas = 3

    mostrar_nivel(screen, nivel, vidas)

    for _ in range(random.randint(3, 5)):
        while True:
            hx = random.randint(50, 750)
            hy = random.randint(50, 550)
            if abs(hx - jugador.rect.centerx) > 80 and abs(hy - jugador.rect.centery) > 80:
                break
        humanos.add(Humano(hx, hy))

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
                pygame.quit()
                exit()
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
        if jugador.disparo_realizado:
            sonido_disparo.play()

        for i, enemigo in enumerate(enemigos):
            if ahora % 2 == i % 2:
                enemigo.update()
        for disparador in disparadores:
            disparador.update()

        bullets.update()
        balas_enemigas.update()
        explosiones.update()
        humanos.update()

        impacto_jugador = pygame.sprite.spritecollide(jugador, balas_enemigas, dokill=True)
        contacto_enemigo = pygame.sprite.spritecollide(jugador, enemigos, dokill=True)
        if contacto_enemigo or impacto_jugador:
            sonido_golpe.play()
            vidas -= 1
            explosiones.add(Explosion(jugador.rect.centerx, jugador.rect.centery))
            if vidas <= 0:
                mostrar_game_over(screen, puntaje, nivel, joystick)
                running = False

        rescatados = pygame.sprite.spritecollide(jugador, humanos, dokill=True)
        puntaje += 1000 * len(rescatados)
        if rescatados:
            sonido_rescate.play()

        for enemigo in enemigos:
            pygame.sprite.spritecollide(enemigo, humanos, dokill=True)
        for disparador in disparadores:
            pygame.sprite.spritecollide(disparador, humanos, dokill=True)

        if enemigos_generados < enemigos_por_nivel and ahora - tiempo_ultimo_spawn > 600:
            while True:
                ex = random.randint(50, 750)
                ey = random.randint(50, 550)
                if abs(ex - jugador.rect.centerx) > 100 and abs(ey - jugador.rect.centery) > 100:
                    break

            if nivel >= 3 and random.random() < 0.2:
                enemigo = EnemigoConversor(ex, ey, jugador, mapa_vacio, humanos, enemigos)
                enemigos.add(enemigo)
            elif nivel >= 2 and random.random() < min(0.2 + nivel * 0.05, 0.5):
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
                sonido_explosion.play()
                explosiones.add(Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                bullet.kill()
            impactos2 = pygame.sprite.spritecollide(bullet, disparadores, dokill=True)
            for enemigo in impactos2:
                sonido_explosion.play()
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
        screen.blit(font.render(f"Puntaje: {puntaje}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Vidas: {vidas}", True, (255, 100, 100)), (10, 40))
        pygame.display.flip()

        if enemigos_generados == enemigos_por_nivel and len(enemigos) + len(disparadores) == 0:
            nivel += 1
            enemigos_por_nivel += 4
            velocidad_base += 0.2
            mostrar_nivel(screen, nivel, vidas)
            enemigos_generados = 0
            tiempo_ultimo_spawn = pygame.time.get_ticks()

            humanos.empty()
            for _ in range(random.randint(3, 5)):
                while True:
                    hx = random.randint(50, 750)
                    hy = random.randint(50, 550)
                    if abs(hx - jugador.rect.centerx) > 80 and abs(hy - jugador.rect.centery) > 80:
                        break
                humanos.add(Humano(hx, hy))

if __name__ == "__main__":
    main()
