import pygame
import sys

pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BG = (169, 255, 156)
COLOR = (255, 97, 48)
player1 = pygame.Rect(0, 0, 100, 100)
player1_image = pygame.image.load('steve.png')
player1_image = pygame.transform.scale(player1_image, (player1.width, player1.height))
player2 = pygame.Rect(400, 400, 100, 100)
player2_image = pygame.image.load('ball.png')
player2_image = pygame.transform.scale(player2_image, (player2.width, player2.height))
direction1 = 'none'
direction2 = 'none'
while True:
    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction1 = 'right'
            elif event.key == pygame.K_LEFT:
                direction1 = 'left'
            elif event.key == pygame.K_UP:
                direction1 = 'up'
            elif event.key == pygame.K_DOWN:
                direction1 = 'down'
            elif event.key == pygame.K_d:
                direction2 = 'right2'
            elif event.key == pygame.K_a:
                direction2 = 'left2'
            elif event.key == pygame.K_w:
                direction2 = 'up2'
            elif event.key == pygame.K_s:
                direction2 = 'down2'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                direction2 = 'none'
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                direction1 = 'none'


    if direction1 == 'right':
        player1.x += 5
    elif direction1 == 'left':
        player1.x -= 5
    elif direction1 == 'up':
        player1.y -= 5
    elif direction1 == 'down':
        player1.y += 5

    if direction2 == 'right2':
        player2.x += 5
    elif direction2 == 'left2':
        player2.x -= 5
    elif direction2 == 'up2':
        player2.y -= 5
    elif direction2 == 'down2':
        player2.y += 5

    screen.blit(player1_image, player1)
    screen.blit(player2_image, player2)
    pygame.display.update()
    clock.tick(60)
