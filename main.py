import time

import graphics
from Player import Player, Ghost
from Board import Board


if __name__ == '__main__':
    board = Board()
    debug = True
    player_hunt_block_limit = 20

    player = Player(board[4][8])

    ghost1 = Ghost('red', board[0][0], player, path_color=(255, 0, 0), debug=debug, limit=player_hunt_block_limit)
    ghost2 = Ghost('blue', board[16][16], player, path_color=(0, 255, 235), debug=debug, limit=player_hunt_block_limit)
    ghost3 = Ghost('yellow', board[19][5], player, path_color=(255, 217, 0), debug=debug, limit=player_hunt_block_limit)
    ghost4 = Ghost('pink', board[16][0], player, path_color=(255, 61, 245), debug=debug, limit=player_hunt_block_limit)

    ghosts = [ghost1, ghost2, ghost3, ghost4]

    graphics.initialize(player, ghosts, board.nodes)
    graphics.start(debug)

