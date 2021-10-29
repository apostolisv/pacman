from copy import deepcopy

import pygame


class Point:
    big_image = pygame.image.load('assets/general/orb1.png')
    small_image = pygame.image.load('assets/general/orb0.png')
    big_image = pygame.transform.scale(big_image, (25, 25))
    small_image = pygame.transform.scale(small_image, (25, 25))

    def __init__(self, big=False):
        self.big = big

    @property
    def image(self):
        if self.big:
            return self.big_image
        return self.small_image

    @property
    def value(self):
        if self.big:
            return 1
        return 4

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        big = self.__dict__['big']
        setattr(result, 'big', deepcopy(big, memodict))
        return result
