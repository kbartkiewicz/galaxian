import pygame
import sys
import random
import os

pygame.init()

WIDTH, HEIGHT = 1200, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxian")

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (40, 40)
ENEMY_WIDTH, ENEMY_HEIGHT = (40, 30)
HEART_WIDTH, HEART_HEIGHT = (30, 30)
BULLET_WIDTH, BULLET_HEIGHT = (6, 12)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))
SHIP = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'ship.png')),
                              (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
LIFE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'life.png')), (HEART_WIDTH, HEART_HEIGHT))
BLUE_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'blue_enemy.png')),
                                    (ENEMY_WIDTH, ENEMY_HEIGHT))
PINK_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'pink_enemy.png')),
                                    (ENEMY_WIDTH, ENEMY_HEIGHT))
GREEN_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'green_enemy.png')),
                                     (ENEMY_WIDTH, ENEMY_HEIGHT))
RED_ENEMY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'red_enemy.png')),
                                   (ENEMY_WIDTH, ENEMY_HEIGHT))

SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot.mp3'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'start.mp3'))
LVL_COMPLETED_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'lvl_completed.mp3'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'game-over.mp3'))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'victory.mp3'))

FPS = 60

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
DARK_GREY = (96, 96, 96)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)

SMALL_FONT = pygame.font.SysFont('Agency FB', 40)
BIG_FONT = pygame.font.SysFont('Agency FB', 76)


def shot(spaceship, bullets, enemy_bullets, lives):
    EXPLOSION_SOUND.play()
    spaceship.x = 580
    spaceship.y = 620
    pygame.time.delay(1000)
    enemy_bullets.clear()
    bullets.clear()
    lives -= 1
    return lives


def game_over():
    BACKGROUND_SOUND.stop()
    GAME_OVER_SOUND.play()
    return True


def main(level=0, lives=3, max_enemy_bullets=2, enemy_vel=2):
    vel = 4
    bullet_vel = 7

    BACKGROUND_SOUND.play()

    spaceship = pygame.Rect((580, 620), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

    enemies = []
    for i in range(40, 300, 80):
        for j in range(160, 1000, 80):
            enemies.append(pygame.Rect((j, i), (ENEMY_WIDTH, ENEMY_HEIGHT)))

    bullets = []
    enemy_bullets = []
    enemies_colors_list = [BLUE_ENEMY, PINK_ENEMY, GREEN_ENEMY, RED_ENEMY]

    clock = pygame.time.Clock()

    main_menu = False
    win = False
    victory_sound_played = False
    run = True

    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()

        # exiting the game using quit button and firing the bullets using space button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and len(bullets) < 2 and not main_menu:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect((spaceship.x + SPACESHIP_WIDTH / 2 - 3, spaceship.y - 5),
                                               (BULLET_WIDTH, BULLET_HEIGHT)))
                    SHOOT_SOUND.play()

        # ending the game after completing last level
        if level == len(enemies_colors_list):
            BACKGROUND_SOUND.stop()
            main_menu = True
            win = True

        if not main_menu:
            # moving to next level
            if len(enemies) == 0:
                BACKGROUND_SOUND.stop()
                LVL_COMPLETED_SOUND.play()
                pygame.time.delay(2000)
                level += 1
                max_enemy_bullets += 3
                enemy_vel = abs(enemy_vel) + 0.5
                main(level, lives, max_enemy_bullets, enemy_vel)

            # game over after losing all lives
            if lives == 0:
                main_menu = game_over()

            # shooting the bullet by random enemy
            if len(enemy_bullets) < max_enemy_bullets and (len(enemy_bullets) < len(enemies)):
                random_enemy = enemies[random.randint(0, len(enemies)) - 1]
                enemy_bullets.append(pygame.Rect((random_enemy[-4], random_enemy[-3]), (BULLET_WIDTH, BULLET_HEIGHT)))

            # moving the spaceship by pressing buttons
            if keys_pressed[pygame.K_a] and spaceship.x > 0:
                spaceship.x -= vel
            if keys_pressed[pygame.K_d] and spaceship.x + SPACESHIP_WIDTH < WIDTH:
                spaceship.x += vel
            if keys_pressed[pygame.K_s] and spaceship.y + SPACESHIP_HEIGHT < HEIGHT:
                spaceship.y += vel
            if keys_pressed[pygame.K_w] and spaceship.y > 0:
                spaceship.y -= vel

            # moving enemies by enemy velocity value, reducing lives when the spaceship collides with enemy
            # losing the game when any of the enemies touches the bottom of the screen
            for enemy in enemies:
                enemy.x += enemy_vel
                if enemy.colliderect(spaceship):
                    lives = shot(spaceship, bullets, enemy_bullets, lives)
                if enemy.y > HEIGHT - ENEMY_HEIGHT:
                    main_menu = game_over()

            # moving the enemies on screen back and forth
            if max([enemy[-4]] for enemy in enemies)[0] + ENEMY_WIDTH > WIDTH:
                enemy_vel = -enemy_vel
                for enemy in enemies:
                    enemy.y += 10
            if min([enemy[-4]] for enemy in enemies)[0] < 0:
                enemy_vel = -enemy_vel

            # moving the bullets, removing when off-screen and removing bullets and enemies after hitting them
            for bullet in bullets:
                bullet.y -= bullet_vel
                if bullet.y < 0:
                    bullets.remove(bullet)
                for enemy in enemies:
                    if enemy.colliderect(bullet):
                        enemies.remove(enemy)
                        bullets.remove(bullet)

            # moving the enemy bullets, removing when off-screen and reducing lives after hitting a spaceship
            for enemy_bullet in enemy_bullets:
                enemy_bullet.y += bullet_vel
                if enemy_bullet.y > HEIGHT + 200:
                    enemy_bullets.remove(enemy_bullet)
                if enemy_bullet.colliderect(spaceship):
                    lives = shot(spaceship, bullets, enemy_bullets, lives)

            # drawing background and ship
            WIN.blit(BACKGROUND, (0, 0))
            WIN.blit(SHIP, (spaceship.x, spaceship.y))

            # drawing enemies
            for enemy in enemies:
                WIN.blit(enemies_colors_list[level], enemy)

            # drawing bullets
            for bullet in bullets:
                pygame.draw.rect(WIN, YELLOW, bullet)
            for enemy_bullet in enemy_bullets:
                pygame.draw.rect(WIN, RED, enemy_bullet)

            # drawing hearts
            k = 10
            for i in range(lives):
                WIN.blit(LIFE, (k, 640))
                k += 50

        # drawing game-over and victory prompts, victory sound and restarting the game after pressing an "enter"
        else:
            WIN.blit(BACKGROUND, (0, 0))
            if win:
                game_over_text_1 = BIG_FONT.render(f"YOU WIN!", True, WHITE)
                if not victory_sound_played:
                    VICTORY_SOUND.play()
                    victory_sound_played = True
            else:
                game_over_text_1 = BIG_FONT.render(f"GAME OVER", True, WHITE)
            game_over_text_2 = SMALL_FONT.render(f"PRESS ENTER TO PLAY AGAIN", True, WHITE)
            WIN.blit(game_over_text_1,
                     (WIDTH / 2 - game_over_text_1.get_width() / 2, HEIGHT / 2 - game_over_text_1.get_height()))
            WIN.blit(game_over_text_2,
                     (WIDTH / 2 - game_over_text_2.get_width() / 2, HEIGHT / 2))
            if keys_pressed[pygame.K_RETURN]:
                main()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
