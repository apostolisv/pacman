import threading
from typing import List
import pygame
from Player import Player
from Board import Node

screen = None
clock = pygame.time.Clock()

background = pygame.image.load('assets/general/background.png')
background = pygame.transform.scale(background, (600, 600))
animation_counter = 0

player: Player
enemies: List
blocks: List


def initialize(player_, enemies_, blocks_):
    global screen, player, enemies, blocks
    player = player_
    enemies = enemies_
    blocks = blocks_
    pygame.init()
    pygame.display.set_caption('Pacman!')
    screen = pygame.display.set_mode((600, 700))


def draw_blocks():
    s = pygame.Surface((20, 18))
    s.set_alpha(50)
    s.fill((255, 0, 255))
    for row in blocks:
        for b in row:
            if isinstance(b, Node):
                pass
                screen.blit(s, (b.x, b.y))


def draw_portals():
    s = pygame.Surface((50, 30))
    s.fill((0, 0, 0))
    screen.blit(s, (0, 320))
    screen.blit(s, (550, 320))


def draw_entities():
    global animation_counter
    screen.blit(background, (0, 50))
    draw_blocks()

    for enemy in enemies:
        screen.blit(enemy.get_image(animation_counter), (enemy.x, enemy.y))

    screen.blit(player.get_image(animation_counter), (player.x, player.y))
    draw_portals()
    pygame.display.update()
    animation_counter += 1
    if animation_counter > 10:
        animation_counter = 0


def get_enemy_moves():
    [enemy.get_move() for enemy in enemies]


def start():

    running = True

    while running:
        clock.tick(45)
        draw_entities()
        player.move()
        get_enemy_moves()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                    player.direction = 0
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                    player.direction = 1
                if event.key == pygame.K_UP:
                    player.move_up()
                    player.direction = 2
                if event.key == pygame.K_DOWN:
                    player.move_down()
                    player.direction = 3
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = (pygame.mouse.get_pos()[0]+15) // 36
                y = (pygame.mouse.get_pos()[1]) // 30 - 1
                print(x, y)
        pygame.display.update()

