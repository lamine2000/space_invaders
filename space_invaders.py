import time

import pygame as pygame

from mobile.mobile import *

if __name__ == '__main__':
    pygame.init()

    # create window
    screen_width, screen_height = SCREEN_SIZE
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Space Invaders')
    icon = pygame.image.load('resources/images/ufo.png')
    pygame.display.set_icon(icon)
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)

    # play background sound
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)

    # generate 3 lines of enemies
    enemies = []
    enemyY = 0
    enemy_image = pygame.image.load(ENEMY_IMAGE_PATH)

    lost_music_played = False

    for _ in range(NB_LINES_ENEMIES):
        enemyX = 0
        while enemyX < screen_width - enemy_image.get_width():  # line not full
            enemies.append(Enemy((enemyX, enemyY)))
            enemyX += enemy_image.get_width() + 20
        enemyY += enemy_image.get_height() + 20

    # create player
    player_image = pygame.image.load(PLAYER_IMAGE_PATH)
    playerX = screen_width / 2 - player_image.get_width() / 2  # center
    playerY = screen_height - player_image.get_height() - 50  # 50px to bottom
    player = Player((playerX, playerY))

    running = True
    while running:
        time.sleep(.005)
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.manage_keyboard_events(event)

        # updating player, enemies, bullet locations and re-drawing them at their new position
        player.move(screen)
        for bullet in player.bullets:
            bullet.move(screen)
            bullet.kill_enemy(enemies)

        for enemy in enemies:
            enemy.move(screen)
            enemy.kill_player(player)

        enemy_has_escaped = False in [enemy.y < screen_height for enemy in enemies]
        has_lost = enemy_has_escaped or not player.is_alive
        if has_lost and not lost_music_played:
            pygame.mixer.music.load(GAME_OVER_MUSIC)
            pygame.mixer.music.play()
            lost_music_played = True

        pygame.display.update()
