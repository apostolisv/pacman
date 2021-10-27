import time

import graphics
from Player import Player, Ghost
from Board import Board


if __name__ == '__main__':
    board = Board()
    player_block = board[4][8]
    player = Player(player_block)
    ghost1 = Ghost('red', board[0][0], player, depth=10)
    #ghost1 = Ghost('red', board[10][7], player, depth=10)   # depth = how many blocks away a player can be spotted
    #ghost2 = Ghost('blue', board[10][8], player, depth=10)
    #ghost3 = Ghost('yellow', board[10][9], player, depth=10)
    #ghost4 = Ghost('pink', board[11][8], player, depth=10)
    #graphics.initialize(player, [ghost1, ghost2, ghost3, ghost4], board.nodes)
    ghosts = [ghost1]

    graphics.initialize(player, ghosts, board.nodes)
    graphics.draw_entities()
    graphics.start()

