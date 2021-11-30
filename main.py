import math
import pygame
import random
from pygame import mixer

# Initialize
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title & icon
pygame.display.set_caption("Shoot Bugs")
icon = pygame.image.load("Pics/bugIcon.png")
pygame.display.set_icon(icon)

# Background image
bg = pygame.image.load("Pics/background.png")

# Background music
mixer.music.load("Audio/background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Player
playerImg = pygame.image.load("Pics/shooter.png")
playerX = 20  # Constant
playerY = 300
playerSpeed = 0.0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Bugs
bugImg = []
bugX = []
bugY = []
bugSpeed = []
no_of_bugs = 3
for i in range(no_of_bugs):
    bugImg.append(pygame.image.load("Pics/bug.png"))
    bugX.append(random.randint(200, 700))
    bugY.append(random.randint(700, 900))
    bugSpeed.append(0.2)


def bug(a, x, y):
    screen.blit(a, (x, y))


# Bullet
bulletImg = pygame.image.load("Pics/bullet.png")
bulletX = 50
bulletY = playerY
fire = False
bullet_ready = True
bulletSpeed = 0


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


# Collision
def isCollision(x1, y1, x2, y2):
    dist = math.sqrt((math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))
    if dist < 32:
        return True
    return False


# Score and Lives_left
score = 0
lives = 5
font = pygame.font.Font('freesansbold.ttf', 22)
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))


def show_lives(x, y):
    text = font.render("Lives Remaining: " + str(lives), True, (255, 255, 255))
    screen.blit(text, (x, y))


# Game Over
game_over = False


def gameOver():
    text2 = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text2, (200, 250))


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerSpeed = -0.6
            if event.key == pygame.K_DOWN:
                playerSpeed = 0.6
            if event.key == pygame.K_SPACE and not game_over:
                bulletSpeed = 1
                fire = True
                if bullet_ready:
                    bullet_sound = mixer.Sound("Audio/bullet.wav")
                    bullet_sound.play()
                bullet_ready = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerSpeed = 0.0

    # Bullet
    bullet(bulletX, bulletY)
    if not fire:
        bulletY += playerSpeed
    bulletX += bulletSpeed
    if bulletX >= 800:
        bulletX = 50
        bulletSpeed = 0
        fire = False
        bulletY = playerY
        bullet_ready = True
        if not game_over:
            lives -= 1

    # Player
    playerY += playerSpeed
    if playerY <= 0:
        playerY = 0
        bulletY = playerY
    elif playerY >= 472:
        playerY = 472
        bulletY = playerY
    player(playerX, playerY)

    # Bugs
    for i in range(no_of_bugs):
        bug(bugImg[i], bugX[i], bugY[i])
        bugY[i] -= bugSpeed[i]

        if bugY[i] <= -70:
            bugY[i] = random.randint(700, 900)
            bugX[i] = random.randint(200, 700)
            if not game_over:
                lives -= 1

        # Collision
        collision = isCollision(bulletX, bulletY, bugX[i], bugY[i])
        if collision:
            explosion_sound = mixer.Sound("Audio/explosion.wav")
            explosion_sound.set_volume(0.2)
            explosion_sound.play()
            bulletX = 50
            bulletSpeed = 0
            fire = False
            bulletY = playerY
            bugX[i] = random.randint(200, 700)
            bugY[i] = 700
            bullet_ready = True
            score += 1

    show_score(10, 10)
    show_lives(570, 10)

    # Game over
    if lives <= 0:
        for j in range(no_of_bugs):
            bugY[j] = 2000
        gameOver()
        game_over = True
        lives = 0

    pygame.display.update()
