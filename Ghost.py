import math
import pygame
from Player import Player
import random
from collections import deque


class Ghost(Player):
    images = 'assets/ghosts/'
    speed = 1.4

    def __init__(self, color, block, player, path_color, debug=False, limit=20):
        self.images += f'{color}/'
        self.load_images()
        self.player = player
        self.s = pygame.Surface((20, 18))
        self.s.fill(path_color)
        self.debug = debug
        self.limit = limit
        self.spawn = self.block
        super().__init__(block)

    def load_images(self):
        self.right_images = [pygame.image.load(self.images + 'right0.png'), pygame.image.load(self.images + 'right1.png')]
        self.left_images = [pygame.image.load(self.images + 'left0.png'), pygame.image.load(self.images + 'left1.png')]
        self.down_images = [pygame.image.load(self.images + 'down0.png'), pygame.image.load(self.images + 'down1.png')]
        self.up_images = [pygame.image.load(self.images + 'up0.png'), pygame.image.load(self.images + 'up1.png')]

    def get_move(self, screen):

        if self.direction not in self.available_moves() or random.randint(0, 100) < 3:
            self.direction = random.randint(0, 3)
        if self.player.move_enemies():
            path = a_star_search(self.block, self.player.block, manhattan_distance)
            if path:
                self.speed = 1.8
                next_node = path[0]
                direction = get_direction(self.block, next_node)
                if len(path) < self.limit:
                    self.direction = direction
                if self.debug:
                    for node in path:
                        screen.blit(self.s, (node.x, node.y))
            else:
                self.speed = 1.4
            self.move()

    def move(self):
        super().move()
        if self.block == self.player.block:
            self.player.kill()


def get_direction(start, block):
    """
    :param start: Board.Node object
    :param block: Board.Node object
    :return: returns 0/1/2/3/4 if start is left/right/above/below the block
    """
    x_start, y_start = start.coords
    x_end, y_end = block.coords
    if x_start == x_end:    # same row
        return 0 if y_start > y_end else 1
    else:   # same column
        return 2 if x_start < x_end else 3


def a_star_search(start, goal, heuristic):
    """
    :param start: Board.Node object
    :param goal: Board.Node object
    :param heuristic: heuristic function
    :return: a list of Board.Node objects that represents a path from the start node to the finish node
    """
    start_node = PathNode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = PathNode(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    open_list = deque([start_node])
    closed_list = deque()

    while 50 > len(open_list) > 0:
        open_list = sorted(open_list, key=lambda x: x.f, reverse=True)  # key: f = g + h
        current = open_list.pop()
        closed_list.append(current)

        if current == end_node:
            path = []
            current_node = current
            while current_node is not None:
                path.append(current_node.node)
                current_node = current_node.parent
            return path[::-1][1:]

        neighbours = get_neighbours(current)
        children = []
        for n in neighbours:
            children.append(PathNode(current, n))

        for child in children:
            for c in closed_list:
                if child == c:
                    continue
            child.g = current.g + 1
            child.h = heuristic(child.node, goal)
            child.f = child.g + child.h

            for n in open_list:
                if child == n and child.g > n.g:
                    continue
            open_list.append(child)

    return False


class PathNode:
    """
    PathNode object is used to 'pack' Board.Node objects with their 'parents' for the a* algorithm
    """
    def __init__(self, parent=None, node=None):
        self.parent = parent
        self.node = node

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.node == other.node


def get_neighbours(path_node):
    """
    :param path_node: Board.Node object
    :return: a list of it's existing neighbours
    """
    block = path_node.node
    blocks = [block.up, block.down, block.left, block.right]
    return [b for b in blocks if b is not None]


def manhattan_distance(start, finish):
    """
    :param start: Board.Node object
    :param finish: Board.Node object
    :return: manhattan distance of the two nodes
    """
    return abs(start.x - finish.x) + abs(start.y - finish.y)


def euclidean_distance(start, finish):
    """
    :param start: Board.Node object
    :param finish: Board.Node object
    :return: euclidean distance of the two nodes
    """
    return math.sqrt(math.pow((start.x - finish.x), 2) + math.pow((start.x - finish.x), 2))


def chebyshev_distance(start, finish):
    """
    (Best results in the least possible iterations for a*)
    :param start: Board.Node object
    :param finish: Board.Node object
    :return: chebyshev distance of the two nodes
    """
    return max(abs(finish.y - start.y), abs(finish.x - start.x))