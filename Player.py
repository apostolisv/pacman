import random

import pygame
from collections import deque

class Player:

    images = 'assets/player/'
    right_images = [pygame.image.load(images + 'alive/right0.png'), pygame.image.load(images + 'alive/right1.png')]
    left_images = [pygame.image.load(images + 'alive/left0.png'), pygame.image.load(images + 'alive/left1.png')]
    down_images = [pygame.image.load(images + 'alive/down0.png'), pygame.image.load(images + 'alive/down1.png')]
    up_images = [pygame.image.load(images + 'alive/up0.png'), pygame.image.load(images + 'alive/up1.png')]

    left = False
    right = False
    up = False
    down = False
    direction = -1  # 0: left | 1: right | 2: up | 3: down
    speed = 2.2

    def __init__(self, block, enemy_spawn_access=False):
        self.block = block
        self.x = block.x
        self.y = block.y
        self.scale_images()

    def move(self):
        if self.left or (self.direction == 0 and self.block.left):
            self.move_left()
        if self.right or (self.direction == 1 and self.block.right):
            self.move_right()
        if self.up or (self.direction == 2 and self.block.up):
            self.move_up()
        if self.down or (self.direction == 3 and self.block.down):
            self.move_down()

    def available_moves(self):
        moves = []
        if self.block.left:
            moves.append(0)
        if self.block.right:
            moves.append(1)
        if self.block.up:
            moves.append(2)
        if self.block.down:
            moves.append(3)
        return moves

    def move_enemies(self):
        return self.direction != -1

    def move_right(self):
        if self.block.right:
            self.y = self.block.y
            self.reset_directions()
            self.right = True
            if self.x + 5 < self.block.right.x:
                self.x += self.speed
            else:
                self.block = self.block.right
                self.x = self.block.x

    def move_left(self):
        if self.block.left:
            self.y = self.block.y
            self.reset_directions()
            self.left = True
            if self.x - 5 > self.block.left.x:
                self.x -= self.speed
            else:
                self.block = self.block.left
                self.x = self.block.x

    def move_up(self):
        if self.block.up:
            self.x = self.block.x
            self.reset_directions()
            self.up = True
            if self.y - 5 > self.block.up.y:
                self.y -= self.speed
            else:
                self.block = self.block.up
                self.y = self.block.y

    def move_down(self):
        if self.block.down:
            self.x = self.block.x
            self.reset_directions()
            self.down = True
            if self.y + 5 < self.block.down.y:
                self.y += self.speed
            else:
                self.block = self.block.down
                self.y = self.block.y

    def scale_images(self):
        for c in [self.right_images, self.left_images, self.down_images, self.up_images]:
            for i in range(2):
                c[i] = pygame.transform.scale(c[i], (25, 25))

    def get_image(self, counter):
        if counter < 5:
            val = 0
        else:
            val = 1
        if self.left:
            return self.left_images[val]
        if self.down:
            return self.down_images[val]
        if self.up:
            return self.up_images[val]
        return self.right_images[val]

    def reset_directions(self):
        self.up = self.down = self.left = self.right = False


class Ghost(Player):
    images = 'assets/ghosts/'
    speed = 1.8

    def __init__(self, color, block, player, depth):
        self.images += f'{color}/'
        self.load_images()
        self.player = player
        self.depth = depth
        super().__init__(block, enemy_spawn_access=True)

    def load_images(self):
        self.right_images = [pygame.image.load(self.images + 'right0.png'), pygame.image.load(self.images + 'right1.png')]
        self.left_images = [pygame.image.load(self.images + 'left0.png'), pygame.image.load(self.images + 'left1.png')]
        self.down_images = [pygame.image.load(self.images + 'down0.png'), pygame.image.load(self.images + 'down1.png')]
        self.up_images = [pygame.image.load(self.images + 'up0.png'), pygame.image.load(self.images + 'up1.png')]

    def get_move(self):

        if self.direction not in self.available_moves() or random.randint(0, 100) < 2:
            self.direction = random.randint(0, 3)
        if self.player.move_enemies():
            test = a_star_search(self.block, self.player.block)
            print(test)
            #self.move()


def a_star_search(start, goal):

    start_node = PathNode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = PathNode(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    open_list = deque([start_node])
    closed_list = deque()

    while 150 > len(open_list) > 0:
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
            child.h = manhattan_distance(child.node, goal)
            child.f = child.g + child.h

            for n in open_list:
                if child == n and child.g > n.g:
                    continue

            open_list.append(child)
    return False


class PathNode:

    def __init__(self, parent=None, node=None):
        self.parent = parent
        self.node = node

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.node == other.node


def get_neighbours(path_node):
    block = path_node.node
    blocks = [block.up, block.down, block.left, block.right]
    return [b for b in blocks if b is not None]


def manhattan_distance(start, finish):
    return abs(start.x - finish.x) + abs(start.y - finish.y)
