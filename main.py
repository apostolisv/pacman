import graphics
from Player import Player
from Board import Board

if __name__ == '__main__':
    board = Board()
    block = board[4][8]
    player = Player(block)
    graphics.initialize(player, [], board.nodes)
    graphics.draw_entities()

    graphics.start()
