# Pong Game
# This code is NOT original
# This code was written by following a tutorial by Clear Code
# Youtube link: https://www.youtube.com/watch?v=Qf3-aDXG8q4
# Github: https://github.com/clear-code-projects/Pong_in_Pygame

# Drawing in Pygame
# first, create a display surface object
# you can have as many regular surfaces on your display surface
# you can put a Rect around shapes to make them easier to measure and manipulate

import pygame
import random

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # wall collisions
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()
    # pad collisions
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top -= opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

# Setup
pygame.init() #initiates all the pygame modules
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 900
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game shapes
ballsize = 30
playerLength = 140
wallOffset = 20
padThickness = 10
ball = pygame.Rect(screen_width/2-ballsize/2, screen_height/2-ballsize/2,ballsize,ballsize)
player = pygame.Rect(screen_width - wallOffset, screen_height/2 - playerLength/2, padThickness, playerLength)
opponent = pygame.Rect(wallOffset/2, screen_height/2 - playerLength/2, padThickness, playerLength)

bg_color = pygame.Color('grey12') # background color
light_grey = (200,200,200)

ball_speed_x = 7 * random.choice([-1, 1])
ball_speed_y = 7 * random.choice([-1, 1])
player_speed = 0
opponent_speed = 7 * random.choice([-1, 1])

# Loop
while True:
    # Handling input
    for event in pygame.event.get(): # pygame calls all user-interactions events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
    ball_animation()
    opponent_animation()
    player_animation()

    # visuals (are drawn in the order they are coded)
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Updating the window
    pygame.display.flip() # take everything that came before it in the loop and draw a picture from that
    clock.tick(60) # how fast the loop runs. Here it is 60 fps
