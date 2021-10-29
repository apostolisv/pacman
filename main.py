import graphics
from Player import Player
from Ghost import Ghost
from Board import Board


if __name__ == '__main__':

    board = Board()
    debug = False
    player_hunt_block_limit = 8
    keep_playing = True

    while keep_playing:
        player = Player(board[4][8])
        board.spawn_points()

        ghost1 = Ghost('red', board[10][7], player, path_color=(255, 0, 0), spawn=board[11][8], debug=debug, limit=player_hunt_block_limit)
        ghost2 = Ghost('blue', board[10][8], player, path_color=(0, 255, 235), spawn=board[11][8], debug=debug, limit=player_hunt_block_limit)
        ghost3 = Ghost('yellow', board[10][9], player, path_color=(255, 217, 0),spawn=board[11][8],  debug=debug, limit=player_hunt_block_limit)
        ghost4 = Ghost('pink', board[11][8], player, path_color=(255, 61, 245), spawn=board[11][8], debug=debug, limit=player_hunt_block_limit)

        ghosts = [ghost1, ghost2, ghost3, ghost4]
        player.ghosts = ghosts

        graphics.initialize(player, ghosts, board)
        keep_playing = graphics.start(debug)

