from copy import deepcopy
from itertools import chain
from Point import Point
from maps import Map


class Board:

    def __init__(self, game_map: Map):
        self.game_map = game_map

    def game_over(self):
        return self.game_map.game_over()

    def spawn_points(self):
        self.game_map.spawn_points()

    @property
    def nodes(self):
        return self.game_map.nodes

    def __getitem__(self, item):
        return self.game_map[item]