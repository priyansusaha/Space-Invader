import pygame
from pygame import mixer
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("img/background.png")

mixer.music.load('sfx/background.wav')
mixer.music.play(-1)

playerImg = pygame.image.load('img/airplane.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg1 = pygame.image.load('img/alien1.png')
enemyImg2 = pygame.image.load('img/alien2.png')
enemyImg3 = pygame.image.load('img/alien3.png')
enemyImg = [enemyImg1, enemyImg2, enemyImg3]
enemyImgR = enemyImg[random.randint(0, 2)]
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 400)
enemyX_change = 3
enemyY_change = 40
enemy_num = 1

bulletImg = pygame.image.load('img/missile.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = False

explosion = pygame.image.load('img/explosion.png')

score = 0
font = pygame.font.Font('font/Wild Hazelnut.TTF', 32)
font2 = pygame.font.Font('font/Wild Hazelnut.TTF', 200)
textX = 10
textY = 10


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImgR, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score_p = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_p, (x, y))

def game_over(x, y):
    gameover = font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameover, (x, y))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == False:
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('sfx/laser.wav')
                    bullet_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX >= 800 - 64:
        playerX = 800 - 64
    elif playerX <= 0:
        playerX = 0

    enemyX += enemyX_change
    if enemyX >= 800 - 64:
        enemyX_change = -4
        enemyY += enemyY_change
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    if enemyX == playerX and enemyY == playerY:
        game_over(10,10)


    if bulletY <= 0:
        bulletY = 480
        bullet_state = False
    if bullet_state is True:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    collision = isCollison(enemyX, enemyY, bulletX, bulletY)
    if collision:
        screen.blit(explosion, (enemyX, enemyY))
        pygame.time.wait(750)
        enemy_num += 1
        bulletY = 480
        bullet_state = False
        score += 10
        enemyX = random.randint(0, 736)
        enemyY = 50
        explosion_sound = mixer.Sound('sfx/explosion.wav')
        explosion_sound.play()

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)
    pygame.display.update()
