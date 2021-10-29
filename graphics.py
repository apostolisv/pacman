from Board import Board
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
board: Board
game_over_text: str
score_text: str

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)


def initialize(player_, enemies_, board_):
    global screen, player, enemies, blocks, game_over_text, board, score_text
    player = player_
    enemies = enemies_
    blocks = board_.nodes
    board = board_
    pygame.init()
    pygame.display.set_caption('Pacman!')
    screen = pygame.display.set_mode((600, 700))
    game_over_text = font.render('GAME OVER! PRESS "SPACE" TO RESTART!', False, (237, 237, 237))
    score_text = font.render('SCORE 0', False, (237, 237, 237))


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


def draw_points():
    for node_list in blocks:
        for b in node_list:
            if b and b.point:
                screen.blit(b.point.image, (b.x, b.y))


def draw_score():
    global score_text
    s = pygame.Surface((60, 30))
    s.fill((0, 0, 0))
    screen.blit(s, (95, 10))
    score_text = font.render(f'SCORE {player.points}', False, (237, 237, 237))
    screen.blit(score_text, (25, 15))


def draw_entities(debug):
    global animation_counter
    screen.blit(background, (0, 50))
    if debug:
        draw_blocks()
    draw_points()
    for enemy in enemies:
        screen.blit(enemy.get_image(animation_counter), (enemy.x, enemy.y))

    screen.blit(player.get_image(animation_counter), (player.x, player.y))
    draw_portals()
    pygame.display.update()
    animation_counter += 1
    if animation_counter > 10:
        animation_counter = 0


def get_enemy_moves():
    [enemy.get_move(screen) for enemy in enemies]


def get_player_move():
    if player.alive:
        player.move()


def game_over():
    return not player.alive or board.game_over()


def draw_game_over():
    screen.blit(game_over_text, (80, 660))


def start(debug):

    while True:
        clock.tick(45)
        draw_entities(debug)
        get_player_move()
        get_enemy_moves()
        draw_score()
        if game_over():
            draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if not game_over():
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
            if event.type == pygame.MOUSEBUTTONDOWN and debug:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                print((x, y))

        pygame.display.update()

