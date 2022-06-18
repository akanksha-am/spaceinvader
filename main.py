import pygame
import random
import math
from pygame import mixer
# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# if we write just this then window with width,height 800*600pixels will close within few secs,we need to make it stay unyil we press cross button
# background
background = pygame.image.load('bg.jpg')

#BG sound
mixer.music.load('background.wav')
#we use music coz we need this for long, but for bullet short music is required so there we use sound
mixer.music.play(-1)
# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load('player.png')
# to define the coordinates where the image will be loaded
playerX = 360
playerY = 470
playerX_change = 0
# enemy
# we are creating list of enemies
enemyImg = []
enemyY = []
enemyX = []
enemyX_change = []
enemyY_change = []
n = 6
# total no. of enemies

for i in range(n):
    enemyImg.append(pygame.image.load('alien.png'))
    # using append we are putting all values of the variables inside the list
    # to define the coordinates where the image will be loaded
    enemyX.append(random.randint(0, 735))
    # we want enemy to appear in any random place in x axis between 0 - 800, it generates any random number,it moves anywhere
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    # we gave this 0.3 so that it starts moving on its own when we call enemy function as we do enemyX+=enemyXchange
    enemyY_change.append(40)

# ready = cant see bullet on screen
# fire= bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
# coz bullet will be at position of 480 where the player is situated
bulletY_change = 1
# we want it to move in y direction
bullet_state = "ready"

#score
score=0
#this value gets incremented everytime bullet hits enemy
#font of score
font=pygame.font.Font('Gelato.ttf', 40)
textX=10
texty=10

#Game Over Text
over_font=pygame.font.Font('Shiny Signature.ttf', 80)

def showscore(x,y):
    # we are rendering text on screen,1st score typecasted to string,True and giving color for text
    scoreS=font.render("Score:" + str(score),True,(255,150,0))
    screen.blit(scoreS, (x, y))

def game_over():
    over_text=over_font.render("GAME OVER",True,(255,0,255))
    screen.blit(over_text, (200,250))

def player(x, y):
    # blit function means to draw on the screen containig the image and the coordinates
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit function means to draw on the screen containig the image and the coordinates
    screen.blit(enemyImg[i], (x, y))
    #as there are 6 enemies so we need to specify which image we need to bliy with [i] & for tat an argument i is specified


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    # x+16 and y+10 because the bullet we want on centre of player(x) and above player(y)


# is the bullet colliding with the enemy or not
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 20:
        return True
    else:
        return False


running = True
# game loop
while running:
    # rgb=red green blue,max=255,this is for background, as we want this to persist throughout we put this in while loop
    screen.fill((255, 0, 255))
    # background image
    screen.blit(background, (0, 0))
    # every key stroke is an event which gets locked in pygame.event.get()
    for event in pygame.event.get():
        # all the events happening inside the pygame window
        if event.type == pygame.QUIT:
            running = False
            # make it false when we press cross button in the window
        # in the event check if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            print("Keystroke pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
                print("Left arrow pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
                print("Right arrow pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # we can fire bullet only if it is ready state means bullet goes beyond y coordinate, then next one fires
                    bulletX = playerX
                    # now use bulletX everywhere whose value wont change with change in playerX & bullet moves in straight line & dont move with player
                    fire_bullet(bulletX, bulletY)
                    #bullet sound
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
        # check whether keystroke released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                # so that after releasing keystroke player stops moving like 0.1 stops getting added or subtracted
                print("Released")
    playerX += playerX_change
    # checking for boundaries so that it doesnt go out of bounds
    if (playerX < 0):
        playerX = 0
    elif (playerX > 736):
        # 736 bcz our player is of 64*64 pixels ,so 800-64=736
        playerX = 736
    # Enemy movement
    # for all the 6 enemies
    for i in range(n):

        #game over
        if enemyY[i]>460:
        #if one enemy reaches there
            for j in range(n):
                #we will move all the enemies one by one completely down out of the screen
                enemyY[j]=2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        # so that it continuously moves

        if (enemyX[i] <= 0):
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
            # if it hits boundary,it will move down by 40 pixels which we kept in enemyYChange
        elif (enemyX[i] >= 736):
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]
            # collision should also be placed here as we need to check collision for each of the 6 enemies so copy paste
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            # it gets incremented every time the bullet hits the enemy
            print(score)
            # so that after getting hitted it respons back to starting
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
        # so while blitting image above we need to write i there also
    # calling player function after screen filling is done
    player(playerX, playerY)

    # bullet movement
    if bulletY <= 0:
        # so that more than one bullet can be fired
        bulletY = 480
        bullet_state = "ready"
        # so that it comes out of loop and resets back to original position,again when spacebar pressed then sets to fire
    if bullet_state is "fire":
        # state is fire means we have called the function when spacebar is pressed
        # again we have to write this after event for loop so that it keeps on firing
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        # if x coordinate is playerX which changes when arrow keys pressed
    showscore(textX,texty)
    # we need to update the display(game window which is screen variable)in every game so that everything gets updated
    pygame.display.update()
