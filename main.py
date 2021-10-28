import time

import graphics
from Player import Player, Ghost
from Board import Board


if __name__ == '__main__':
    board = Board()
    player_block = board[4][8]
    player = Player(player_block)
    ghost1 = Ghost('red', board[0][0], player, path_color=(255, 0, 0))
    #ghost1 = Ghost('red', board[10][7], player, depth=10)   # depth = how many blocks away a player can be spotted
    ghost2 = Ghost('blue', board[16][16], player, path_color=(0, 255, 235))
    ghost3 = Ghost('yellow', board[19][5], player, path_color=(255, 217, 0))
    ghost4 = Ghost('pink', board[16][0], player, path_color=(255, 61, 245))
    #graphics.initialize(player, [ghost1, ghost2, ghost3, ghost4], board.nodes)
    ghosts = [ghost1, ghost3]

    graphics.initialize(player, ghosts, board.nodes)
    graphics.draw_entities()
    graphics.start()

