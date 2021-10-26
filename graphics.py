from typing import List

import pygame
from Player import Player
from Ghost import Ghost
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
    s = pygame.Surface((24, 22))
    s.set_alpha(50)
    s.fill((255, 0, 255))
    for row in blocks:
        for b in row:
            if isinstance(b, Node):
                screen.blit(s, (b.x, b.y))


def draw_entities():
    global animation_counter
    screen.blit(background, (0, 50))
    draw_blocks()
    screen.blit(player.get_image(animation_counter), (player.x, player.y))
    pygame.display.update()

    animation_counter += 1
    if animation_counter > 10:
        animation_counter = 0


def start():

    running = True
    while running:
        clock.tick(45)
        draw_entities()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_UP:
                    player.move_up()
                if event.key == pygame.K_DOWN:
                    player.move_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                pygame.display.update()
