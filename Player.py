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
            test = self.a_star_search(self.player.block)
            #self.move()

    def a_star_search(self, goal):
        open_list = deque([(self.block, 0, self.manhattan_distance(self.block, self.player))])
        closed_list = deque()

        while len(open_list) > 0:
            open_list = sorted(open_list, key=lambda x: x[1]+x[2], reverse=True)  # key: f = g + h
            current = open_list.pop()
            if current[0] == goal:
                return True
            closed_list.append(current)
            neighbours = self.neighbours(current, goal)
            for n in neighbours:
                pass
        return False

    def neighbours(self, block_tuple, finish):
        block = block_tuple[0]
        blocks = [block.up, block.down, block.left, block.right]
        return [(b, block_tuple[1] + 1, self.manhattan_distance(b, finish)) for b in blocks if b is not None]

    def manhattan_distance(self, start, finish):
        return abs(start.x - finish.x) + abs(start.y - finish.y)
