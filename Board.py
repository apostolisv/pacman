from Ghost import Ghost
from Player import Player
from maps import Map


class Board:

    def __init__(self, game_map: Map, player: Player, ghosts: list[Ghost]):
        self.game_map = game_map
        self.player = player
        self.ghosts = ghosts

    def get_player_move(self):
        if self.player.alive:
            self.player.move()

    def get_enemy_moves(self, screen):
        if self.player.move_enemies():
            [ghost.get_move(screen, self.player) for ghost in self.ghosts]

    def tick(self, screen):
        self.get_player_move()
        self.get_enemy_moves(screen)

        if self.player.block.point:
            self.player.points += self.player.block.point.value
            if self.player.block.point.big:
                [g.make_vulnerable() for g in self.ghosts]
            self.player.block.point = None

        for g in self.ghosts:
            if g.block == self.player.block:
                if g.vulnerable:
                    g.kill()
                    self.player.points += 50
                elif g.alive:
                    self.player.kill()

    def game_over(self):
        return self.game_map.game_over()

    def spawn_points(self):
        self.game_map.spawn_points()

    def get_background(self):
        return self.game_map.get_background()

    @property
    def nodes(self):
        return self.game_map.nodes

    def __getitem__(self, item):
        return self.game_map[item]
