import math

import pygame


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

    speed = 2.2

    def __init__(self, block):
        self.block = block
        self.x = block.x
        self.y = block.y
        self.scale_images()

    def move(self):
        if self.left:
            self.move_left()
        if self.right:
            self.move_right()
        if self.up:
            self.move_up()
        if self.down:
            self.move_down()
        self.reset_directions()

    def move_right(self):
        if self.block.right:
            self.reset_directions()
            self.right = True
            self.block = self.block.right
            self.x = self.block.x

    def move_left(self):
        if self.block.left:
            self.reset_directions()
            self.left = True
            self.block = self.block.left
            self.x = self.block.x

    def move_up(self):
        if self.block.up:
            self.reset_directions()
            self.up = True
            self.block = self.block.up
            self.y = self.block.y

    def move_down(self):
        if self.block.down:
            self.reset_directions()
            self.down = True
            self.block = self.block.down
            self.y = self.block.y

    def scale_images(self):
        for c in [self.right_images, self.left_images, self.down_images, self.up_images]:
            for i in range(2):
                c[i] = pygame.transform.scale(c[i], (30, 30))

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
