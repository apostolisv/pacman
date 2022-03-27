from itertools import chain
from abc import ABC

import pygame

from Point import Point


class Map(ABC):

    nodes = []

    def __init__(self):
        pass

    def create_nodes(self):
        pass

    def link_nodes(self):
        self.link_nodes_horizontally()
        self.link_nodes_vertically()

    def link_nodes_horizontally(self):
        for line in self.nodes:
            for i in range(1, len(line)):
                if isinstance(line[i-1], Node) and isinstance(line[i], Node):
                    line[i-1].right = line[i]
                    line[i].left = line[i-1]

    def link_nodes_vertically(self):
        for i in range(1, len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if isinstance(self.nodes[i - 1][j], Node) and isinstance(self.nodes[i][j], Node):
                    self.nodes[i - 1][j].up = self.nodes[i][j]
                    self.nodes[i][j].down = self.nodes[i - 1][j]

    def spawn_points(self):
        pass

    def delete_excess_nodes(self):
        pass

    def get_enemy_spawns(self):
        pass

    def get_player_spawn(self):
        pass

    def delete_(self, places):
        for place in places:
            index = place[0]
            for column in place[1]:
                self.nodes[index][column] = None

    def game_over(self):
        pass

    def get_background(self):
        pass

    def __getitem__(self, item):
        return self.nodes[item]


class Map1(Map):

    def __init__(self):
        super().__init__()
        self.nodes.extend([[''] for _ in range(20)])
        self.create_nodes()
        self.link_nodes()

    def create_nodes(self):
        for i in range(20):
            for j in range(9):
                node = Node(14 + 34.5 * j, 613 - i * 29, (i, j))
                if isinstance(self.nodes[i][-1], Node):
                    self.nodes[i].append(node)
                else:
                    self.nodes[i][0] = node
        self.delete_excess_nodes()
        for i in range(len(self.nodes)):
            for node in self.nodes[i][:-1]:
                if isinstance(node, Node):
                    self.nodes[i].extend([Node(578-node.x, node.y, (node.coords[0], 16-node.coords[1]))])
                else:
                    self.nodes[i].extend([''])
        self.rearrange_nodes()
        self.nodes[12][8].special_access_down = True
        self.nodes[11][8].special_access_down = True
        self.nodes[10][8].special_access_right = True
        self.nodes[10][8].special_access_left = True

    def link_nodes(self):
        super().link_nodes()
        self.nodes[10][0].left = self.nodes[10][-1]
        self.nodes[10][-1].right = self.nodes[10][0]

    def rearrange_nodes(self):
        for line in self.nodes:
            line[9:] = line[9:][::-1]

    def delete_excess_nodes(self):
        self.delete_([[1, chain(range(1, 7), range(8, 9))], [2, range(4, 9, 4)], [3, (0, 2, 4, 6, 7, 8)]])
        self.delete_([[4, [2]], [5, chain(range(1, 3), range(4, 7), [8])], [6, [8]]])
        self.delete_([[7, chain(range(3), [4], range(6, 9))], [8, chain(range(3), [4])]])
        self.delete_([[9, chain(range(3), [4], range(6, 9))], [10, [6]], [11, chain(range(3), [4], range(6, 8))]])
        self.delete_([[12, chain(range(3), [4])], [13, chain(range(3), range(4, 7), [8])]])
        self.delete_([[14, [4, 8]], [15, [1, 2, 4, 6, 7, 8]], [17, [1, 2, 4, 5, 6, 8]], [18, [1, 2, 4, 5, 6, 8]]])
        self.delete_([[19, [8]]])

    def spawn_points(self):
        for node_list in self.nodes:
            for node in node_list:
                if node:
                    if 13 > node.coords[1] > 3 and 6 < node.coords[0] < 14 or node.coords[0] == 10 and (node.coords[1] < 3 or node.coords[1] > 13):
                        node.point = None
                    else:
                        node.point = Point()
        self.nodes[4][0].point.big = True
        self.nodes[4][-1].point.big = True
        self.nodes[17][0].point.big = True
        self.nodes[17][-1].point.big = True
        self.nodes[4][8].point = None

    def player_spawn(self):
        return self.nodes[4][8]

    def enemy_spawns(self):
        g1 = self.nodes[10][7]
        g2 = self.nodes[10][8]
        g3 = self.nodes[10][9]
        g4 = self.nodes[11][8]
        return g1, g2, g3, g4

    def enemy_spawn_entrance(self):
        return self.nodes[11][8]

    def get_background(self):
        background = pygame.image.load('assets/general/background.png')
        background = pygame.transform.scale(background, (600, 600))
        return background

    def game_over(self):
        total = 0
        for node_list in self.nodes:
            for node in node_list:
                if node and node.point:
                    total += 1
        return total == 0


class Node:

    right = left = down = up = None
    special_access_down = special_access_left = special_access_right = False

    point = None

    def __init__(self, x, y, coords, point=None):
        self.x = x
        self.y = y
        self.coords = coords
        self.point = point

    def check_down(self, player=None):
        if self.special_access_down:
            return self.down if player and not player.alive else None
        return self.down

    def check_left(self, player=None):
        if self.special_access_left:
            return self.left if player and not player.alive else None
        return self.left

    def check_right(self, player=None):
        if self.special_access_right:
            return self.right if player and not player.alive else None
        return self.right

    def __repr__(self):
        return f'Node({self.coords})[{self.x}, {self.y}]'
