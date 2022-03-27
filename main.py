import graphics
from Player import Player
from Ghost import Ghost
from Board import Board
from maps import Map1

if __name__ == '__main__':

    game_map = Map1()
    player_spawn = game_map.player_spawn()
    enemy_spawns = game_map.enemy_spawns()
    enemy_spawn_entrance = game_map.enemy_spawn_entrance()
    board = Board(game_map)
    debug = True
    hunt_limit = 8
    keep_playing = True

    while keep_playing:
        player = Player(player_spawn)
        board.spawn_points()

        ghost1 = Ghost('red', enemy_spawns[0], player, path_color=(255, 0, 0), spawn=enemy_spawn_entrance, debug=debug, limit=hunt_limit)
        ghost2 = Ghost('blue', enemy_spawns[1], player, path_color=(0, 255, 235), spawn=enemy_spawn_entrance, debug=debug, limit=hunt_limit)
        ghost3 = Ghost('yellow', enemy_spawns[2], player, path_color=(255, 217, 0), spawn=enemy_spawn_entrance,  debug=debug, limit=hunt_limit)
        ghost4 = Ghost('pink', enemy_spawns[3], player, path_color=(255, 61, 245), spawn=enemy_spawn_entrance, debug=debug, limit=hunt_limit)

        ghosts = [ghost1, ghost2, ghost3, ghost4]
        player.ghosts = ghosts

        graphics.initialize(player, ghosts, board)
        keep_playing = graphics.start(debug)

