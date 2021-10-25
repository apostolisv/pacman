import graphics
from Player import Player
import Ghost

if __name__ == '__main__':
    player = Player(285, 440)

    graphics.initialize(player, [])
    graphics.draw_entities()

    graphics.start()
