# this will import pygame functions into our program
import pygame
# this will import a mixer to put music and sounds into the game
from pygame import mixer

# this will import random functions into our program
import random

# this will import math functions
import math

# intialize the pygame
pygame.init()

# create the screen (width * height) 800 for width and 600 for height
screen = pygame.display.set_mode((800, 600))

# adding space background image to the program
background = pygame.image.load('space.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# events are things that happen in the game like pressing a key to quit a game


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('playerShip.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy ship
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemyShip.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 120)


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))
    show_score(textX, textY)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# drawing the image of the player on screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# drawing the image of the player on screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# drawing the bullet on the screen
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB - Red, Green, Blue values 0 - 255
    screen.fill((0, 0, 0))
    # adding the space background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            print("A keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                print("space key has been pressed")
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state == "ready":
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Keystroke has been released")
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    # adding a variable to the x position to change the position, which will move the ship (player movement)
    playerX += playerX_change

    # adding a variable to the x position to change the position, which will move the enemy ship (enemy movement)
    enemyX += enemyX_change

    # calling player function to create the player ship on the screen
    player(playerX, playerY)

    # creating a boundary so that the player ship can't move out of bounce
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement will go backwards when it hits a wall
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:

            if score_value <= 5:
                enemyX_change[i] = 4
            elif score_value <= 10:
                enemyX_change[i] = 6
            elif score_value <= 15:
                enemyX_change[i] = 8
            elif score_value >= 20:
                enemyX_change = 10

            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:

            if score_value <= 5:
                enemyX_change[i] = -4
            elif score_value <= 10:
                enemyX_change[i] = -6
            elif score_value <= 15:
                enemyX_change[i] = -8
            elif score_value >= 20:
                enemyX_change = -10

            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        # calling enemy function to create enemy ship on screen
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)

    # necessary to keep drawing the ship and enemy ship throughout the program (will constantly update program)
    pygame.display.update()
