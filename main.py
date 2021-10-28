import graphics
from Player import Player
from Ghost import Ghost
from Board import Board


if __name__ == '__main__':

    board = Board()
    debug = True
    player_hunt_block_limit = 20
    keep_playing = True
    while keep_playing:
        player = Player(board[4][8])

        ghost1 = Ghost('red', board[10][7], player, path_color=(255, 0, 0), debug=debug, limit=player_hunt_block_limit)
        ghost2 = Ghost('blue', board[10][8], player, path_color=(0, 255, 235), debug=debug, limit=player_hunt_block_limit)
        ghost3 = Ghost('yellow', board[10][9], player, path_color=(255, 217, 0), debug=debug, limit=player_hunt_block_limit)
        ghost4 = Ghost('pink', board[11][8], player, path_color=(255, 61, 245), debug=debug, limit=player_hunt_block_limit)

        ghosts = [ghost1, ghost2, ghost3, ghost4]
        graphics.initialize(player, ghosts, board.nodes)
        keep_playing = graphics.start(debug)

