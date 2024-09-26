import pygame # подключаем библиотеку
import sys # подключаем модуль для 
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
game_state = 0

while True:
    screen.fill((255, 255, 255))
    if game_state == 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    game_state = 1
    
    if game_state == 2:
        screen.fill('red')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player.x, player.y, player.width, player.height = 400, 400, 50, 50
                    enemy.x, enemy.y = 50, 50
                    player_img = pygame.transform.scale(player_img_orig, (player.width, player.height))
                    game_state = 1

    if game_state == 1:
        screen.fill('lightblue')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    direction = 'right'
                elif e.key == pygame.K_LEFT:
                    direction = 'left'
                elif e.key == pygame.K_UP:
                    direction = 'up'
                elif e.key == pygame.K_DOWN:
                    direction = 'down'
            if e.type == pygame.KEYUP:
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


        if player.width >= 100:
            game_state = 2
            
        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)
    pygame.display.update()
    clock.tick(60)
    

