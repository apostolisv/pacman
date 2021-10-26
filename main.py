import graphics
from Player import Player, Ghost
from Board import Board

if __name__ == '__main__':
    board = Board()
    player_block = board[4][8]

    player = Player(player_block)
    ghost1 = Ghost('red', board[10][7], player)
    ghost2 = Ghost('blue', board[10][8], player)
    ghost3 = Ghost('yellow', board[10][9], player)
    ghost4 = Ghost('pink', board[11][8], player)
    graphics.initialize(player, [ghost1, ghost2, ghost3, ghost4], board.nodes)
    graphics.draw_entities()

    graphics.start()
