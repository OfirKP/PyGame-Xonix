# -*- coding: utf-8 -*-
import pygame
from random import randint as rand
from random import choice
from random import choice
import sys

# Constants
STILL = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CORNERS = [(0, 0), (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH - 1, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)]
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):

    def __init__(self, color=WHITE):
        super(Player, self).__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.movement = 0
        self.speed = 3
        self.rect = self.image.get_rect()

        # Randomizing player's location on initial conquered area
        self.rect.x = choice(range(0, 40) + range(SCREEN_WIDTH-50, SCREEN_WIDTH-10))
        self.rect.y = choice(range(0, SCREEN_HEIGHT-10))

        self.points = []
        self.mask = pygame.mask.from_surface(self.image)
        self.in_conquered = False

    def move_right(self, pixels):
        if self.rect.right + pixels >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH - 1
            self.movement = STILL
        else:
            self.rect.x += pixels

    def move_left(self, pixels):
        if self.rect.left - pixels <= 0:
            self.rect.left = 0
            self.movement = STILL
        else:
            self.rect.x -= pixels

    def move_up(self, pixels):
        if self.rect.top - pixels <= 0:
            self.rect.top = 0
            self.movement = STILL
        else:
            self.rect.y -= pixels

    def move_down(self, pixels):
        if self.rect.bottom + pixels >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - 1
        else:
            self.rect.y += pixels

    def change_movement(self, option):
        self.movement = option

    def get_pos(self):
        return list(self.rect.center)

    def add_point(self):
        self.points.append(self.get_pos())

    def update(self, polygon, balls):
        if len(self.points) > 1:
            if not polygon.mask.get_at(self.points[0]):  # Extending first point if floating
                direction = self.line_direction(self.points[0], self.points[1])
                if direction == RIGHT:
                    self.points[0][0] -= 5
                if direction == LEFT:
                    self.points[0][0] += 5
                if direction == DOWN:
                    self.points[0][1] -= 5
                if direction == UP:
                    self.points[0][1] += 5

        if polygon.contains(self):  # If the whole player is inside the conquered area
            if not self.in_conquered:  # If the boolean hasn't been updated
                self.movement = STILL
                self.in_conquered = True
                if len(self.points) >= 2:
                    start_dir = self.line_direction(self.points[0], self.points[1])
                    end_dir = self.line_direction(self.points[-2], self.points[-1])

                    # Drawing trail onto polygon
                    pygame.draw.lines(polygon.image,(0, 255, 0), 0, self.points, 1)
                    polygon.update_mask()

                    '''
                    We decided to divide the work of conquering an area into 2 cases:
                        1. The line is between two opposite walls
                        2. not 1
                    case 2 is more efficient because we can use it to our advantage and extend start and ending points
                    and using pygame's polygon in order to fill it
                    However, case 1 uses an algorithm called flood fill (which is usually done recursively) that is
                    slower but the only reasonable solving.
                    '''
                    if start_dir == end_dir:
                        try:
                            vertical = True if start_dir == 3 or start_dir == 4 else False
                            fill_point = polygon.check_open_sides(self.points, 5, vertical, balls)  # Point of filling
                            polygon.fill_wiki(fill_point[0], fill_point[1], (0, 255, 0))  # Flood fill
                        except:
                            pass
                    else:
                        self.extend_point(self.points[0], start_dir, True)
                        self.extend_point(self.points[-1], end_dir, False)
                        end = (self.points[0][0], self.points[-1][1])
                        if end not in CORNERS:
                            end = (self.points[-1][0], self.points[0][1])
                        self.points.append(end)
                        polygon.add(self.points)
                self.points = []
        elif self.in_conquered and not polygon.mask.get_at(self.get_pos()):  # Player is getting out of conquered area
            self.in_conquered = False
            self.add_point()
            self.add_point()


        if self.movement == RIGHT:
            self.move_right(self.speed)
        elif self.movement == LEFT:
            self.move_left(self.speed)
        elif self.movement == UP:
            self.move_up(self.speed)
        elif self.movement == DOWN:
            self.move_down(self.speed)
        polygon.update_mask()

    def is_self_destruct(self):  # Player overlaps itself
        for i in xrange(len(self.points) - 3):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i+1]
            if min(x1, x2) <= self.points[-1][0] <= max(x1, x2) and min(y1, y2) <= self.points[-1][1] <= max(y1, y2):
                return True
        return False

    def line_direction(self, p1, p2):
        if p1[0] < p2[0]:
            return RIGHT
        elif p1[0] > p2[0]:
            return LEFT
        elif p1[1] > p2[1]:
            return UP
        else:
            return DOWN

    def extend_point(self, p, direction, start):
        if start and direction == RIGHT or not start and direction == LEFT:
            p[0] = 0
        elif start and direction == LEFT or not start and direction == RIGHT:
            p[0] = SCREEN_WIDTH - 1
        elif start and direction == UP or (not start and direction == DOWN):
            p[1] = SCREEN_HEIGHT - 1
        else:
            p[1] = 0