# -*- coding: utf-8 -*-
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WALL_WIDTH = 50

class InversePolygon(pygame.sprite.Sprite):
    def __init__(self, polygon, mask):
        super(InversePolygon, self).__init__()
        self.width = 800
        self.height = 600
        self.image = polygon.image
        self.image.set_colorkey(WHITE)
        self.mask = mask
        self.rect = self.image.get_rect()

    def update_mask(self, mask):
        self.mask = mask
