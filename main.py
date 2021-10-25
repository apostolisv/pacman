import graphics
from Player import Player
from Ghost import Ghost
from Board import Board

if __name__ == '__main__':
    player = Player(285, 440)
    board = Board()
    graphics.initialize(player, [], board.nodes)
    graphics.draw_entities()

    graphics.start()
