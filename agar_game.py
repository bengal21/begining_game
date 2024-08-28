import pygame
import sys
from random import *

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(400, 400, 50, 50)
player_img_orig = pygame.image.load('steve.png')
player_img = pygame.transform.scale(player_img_orig, (player.width, player.height))
enemy = pygame.Rect(50, 50, 30, 30)
enemy_img = pygame.image.load('creeper.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy.width, enemy.height))

direction = 'none'

while True:
    screen.fill('lightblue')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 'right'
            elif event.key == pygame.K_LEFT:
                direction = 'left'
            elif event.key == pygame.K_UP:
                direction = 'up'
            elif event.key == pygame.K_DOWN:
                direction = 'down'
        if event.type == pygame.KEYUP:
            direction = 'none'

    if direction == 'right':
        player.x += 5
    elif direction == 'left':
        player.x -= 5
    elif direction == 'up':
        player.y -= 5
    elif direction == 'down':
        player.y += 5


    if player.colliderect(enemy):
        enemy.x = randint(0, 470)
        enemy.y = randint(0, 470)
        player.width += 5
        player.height += 5
        player_img = pygame.transform.scale(player_img_orig, (player.width, player.height))

    screen.blit(player_img, player)
    screen.blit(enemy_img, enemy)
    pygame.display.update()
    clock.tick(60)

