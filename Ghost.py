import time
import pygame
from maps import Node
from Player import Player
import random
from collections import deque


class Ghost(Player):
    images = 'assets/ghosts/'
    vulnerable_img1 = pygame.image.load('assets/ghosts/ghost00.png')
    vulnerable_img2 = pygame.image.load('assets/ghosts/ghost01.png')
    vulnerable_img3 = pygame.image.load('assets/ghosts/ghost10.png')
    vulnerable_img4 = pygame.image.load('assets/ghosts/ghost11.png')

    vulnerable_img1 = pygame.transform.scale(vulnerable_img1, (25, 25))
    vulnerable_img2 = pygame.transform.scale(vulnerable_img2, (25, 25))
    vulnerable_img3 = pygame.transform.scale(vulnerable_img3, (25, 25))
    vulnerable_img4 = pygame.transform.scale(vulnerable_img4, (25, 25))

    vulnerable_images = [vulnerable_img1, vulnerable_img2, vulnerable_img3, vulnerable_img4]

    dead_img_left = pygame.image.load('assets/ghosts/eyesleft.png')
    dead_img_right = pygame.image.load('assets/ghosts/eyesright.png')
    dead_img_up = pygame.image.load('assets/ghosts/eyesup.png')
    dead_img_down = pygame.image.load('assets/ghosts/eyesdown.png')

    dead_img_left = pygame.transform.scale(dead_img_left, (25, 25))
    dead_img_right = pygame.transform.scale(dead_img_right, (25, 25))
    dead_img_up = pygame.transform.scale(dead_img_up, (25, 25))
    dead_img_down = pygame.transform.scale(dead_img_down, (25, 25))

    dead_images = [dead_img_left, dead_img_right, dead_img_up, dead_img_down]
    speed = 1.4
    _vulnerable = False
    vulnerable_time_start = time.perf_counter()

    def __init__(self, color, block, path_color, spawn, debug=False, limit=20):
        self.images += f'{color}/'
        self.load_images()
        self.s = pygame.Surface((20, 18))
        self.s.fill(path_color)
        self.debug = debug
        self.limit = limit
        super().__init__(block)
        self.spawn = spawn
        self.path = None

    def load_images(self):
        self.right_images = [pygame.image.load(self.images + 'right0.png'), pygame.image.load(self.images + 'right1.png')]
        self.left_images = [pygame.image.load(self.images + 'left0.png'), pygame.image.load(self.images + 'left1.png')]
        self.down_images = [pygame.image.load(self.images + 'down0.png'), pygame.image.load(self.images + 'down1.png')]
        self.up_images = [pygame.image.load(self.images + 'up0.png'), pygame.image.load(self.images + 'up1.png')]

    def make_vulnerable(self):
        self.vulnerable = True
        self.path = None

    @property
    def vulnerable(self):
        return round(time.perf_counter() - self.vulnerable_time_start, 2) < 6 and self._vulnerable

    @vulnerable.setter
    def vulnerable(self, value):
        self.vulnerable_time_start = time.perf_counter()
        self._vulnerable = value

    def get_move(self, screen, player):
        if (self.direction not in self.available_moves() or random.randint(0, 100) < 3) and self.alive:
            self.direction = random.randint(0, 3)
        elif self.alive and not self.vulnerable:
            self.get_path(self.block, player.block, manhattan_distance, screen)
        elif not self.alive:
            if not self.path:
                self.get_path(self.block, self.spawn, chebyshev_distance, screen)
        self.move()

    def get_image(self, counter):
        """
        called by graphics.py in order to draw animations
        :param counter: int 0 < counter < 10
        :return: normal / vulnerable / dead (eyes) asset
        """
        if not self.alive:
            return self.dead_images[self.direction]
        elif self.vulnerable:
            if counter < 2:
                position = 0
            elif counter < 5:
                position = 1
            elif counter < 8:
                position = 2
            else:
                position = 3
            return self.vulnerable_images[position]

        return super().get_image(counter)

    def get_path(self, start, finish: Node, heuristic, screen):
        self.path = a_star_search(start, finish, heuristic, self, screen)
        if self.path:
            next_node = self.path[0]
            direction = get_direction(start, next_node)
            if len(self.path) < self.limit or not self.alive:
                self.speed = 1.8
                self.direction = direction
        else:
            if self.alive:
                self.speed = 1.4
            else:
                finish_neighbours = [finish.left, finish.right, finish.down, finish.up]
                neighbours = random.choice([n for n in finish_neighbours if n is not None])
                self.get_path(start, neighbours, heuristic, screen)

    def move(self):
        super().move()
        if self.block == self.spawn:
            self.alive = True
            self.vulnerable = False
        if not self.alive:
            if self.path and self.path[0] == self.block:
                self.path = None

    def kill(self):
        self.vulnerable = False
        self.alive = False


def get_direction(start, block):
    """
    :param start: maps.Node object
    :param block: maps.Node object
    :return: returns 0/1/2/3/4 if the block object is left/right/above/below of the start object
    """
    x_start, y_start = start.coords
    x_end, y_end = block.coords
    if x_start == x_end:    # same row
        return 0 if y_start > y_end else 1
    else:   # same column
        return 2 if x_start < x_end else 3


def a_star_search(start, goal, heuristic, player, screen):
    start_node = PathNode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = PathNode(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    open_list = deque([start_node])
    closed_list = deque()
    limit = 40 if player.alive else 150
    while limit > len(open_list) > 0:
        open_list = sorted(open_list, key=lambda x: x.f, reverse=True)  # key: f = g + h
        current = open_list.pop()
        closed_list.append(current)

        if player.debug:
            for path_node in open_list:
                screen.blit(player.s, (path_node.node.x, path_node.node.y))
        if current == end_node:
            path = []
            current_node = current
            while current_node is not None:
                path.append(current_node.node)
                current_node = current_node.parent

            if player.debug:
                for node in path:
                    screen.blit(player.s, (node.x, node.y))
            return path[::-1][1:]

        neighbours = get_neighbours(current, player)
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

    return []


class PathNode:

    def __init__(self, parent=None, node=None):
        self.parent = parent
        self.node = node

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.node == other.node


def get_neighbours(block, player):
    if isinstance(block, PathNode):
        block = block.node
    blocks = [block.up, block.check_down(player), block.check_left(player), block.check_right(player)]
    return [b for b in blocks if b is not None]


def manhattan_distance(start, finish):
    return abs(start.x - finish.x) + abs(start.y - finish.y)


def chebyshev_distance(start, finish):
    return max(abs(finish.y - start.y), abs(finish.x - start.x))
