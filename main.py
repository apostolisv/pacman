import graphics
from Player import Player
from Ghost import Ghost
from Board import Board

if __name__ == '__main__':
    board = Board()
    block = board[0][8]
    player = Player(block)
    graphics.initialize(player, [], board.nodes)
    graphics.draw_entities()

    graphics.start()
