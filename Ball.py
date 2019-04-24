# -*- coding: utf-8 -*-
import pygame
from random import randint as rand
from random import choice
import sys

# Constants
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Ball(pygame.sprite.Sprite):

    def __init__(self, radius, velocity=5, alive=True, color=(255, 0, 0)):
        super(Ball, self).__init__()
        self.radius = radius
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.alive = alive  # Alive means whether the ball is on neutral or conquered area

        self.velocity_x = choice([velocity, -velocity])
        self.velocity_y = choice([velocity, -velocity])

        self.rect = self.image.get_rect()
        self.rect.x = rand(50, SCREEN_WIDTH - 50 - 2*radius)
        self.rect.y = rand(50, SCREEN_HEIGHT - 50 - 2 * radius)
        if alive:
            self.color = color
            pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        else:
            self.color = (0, 0, 255)
            # If it is a ghost ball, let it be on a random section of the conquered area
            self.rect.x = rand(0, SCREEN_WIDTH - 1 - 2*radius)
            self.rect.y = choice(range(0, 50 - 2*radius) + range(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 2*radius))
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, 2)

        self.mask = pygame.mask.from_surface(self.image)

    def set_velocity_x(self, v):
        self.velocity_x = v

    def set_velocity_y(self, v):
        self.velocity_y = v

    def update(self, size, polygon):
        if polygon.contains(self) and self.alive:
            #balls.remove(self)
            self.alive = False
            self.image.fill(WHITE)
            pygame.draw.circle(self.image, (0, 0, 255), (self.radius, self.radius), self.radius, 2)
            if self.velocity_x < 0:
                self.velocity_x -= 3
            else:
                self.velocity_x += 3
        if self.alive:
            if self.rect.left + self.velocity_x / 2 < 0 or self.rect.right + self.velocity_x / 2 > size[0] - 1:
                self.velocity_x *= -1
            if self.rect.top + self.velocity_y / 2 < 0 or self.rect.bottom + self.velocity_y / 2 > size[1] - 1:
                self.velocity_y *= -1
            if self.collide_x(polygon):
                self.velocity_x *= -1
            if self.collide_y(polygon):
                self.velocity_y *= -1
            self.rect.x += self.velocity_x / 2
            self.rect.y += self.velocity_y / 2
        else:
            if self.rect.left + self.velocity_x / 2 < 0 or self.rect.right + self.velocity_x / 2 > size[0] - 1:
                self.velocity_x *= -1
            if self.rect.top + self.velocity_y / 2 < 0 or self.rect.bottom + self.velocity_y / 2 > size[1] - 1:
                self.velocity_y *= -1
            if self.collide_x(polygon.polygon_inverse):
                self.velocity_x *= -1
            if self.collide_y(polygon.polygon_inverse):
                self.velocity_y *= -1
            self.rect.x += self.velocity_x / 2
            self.rect.y += self.velocity_y / 2

    # To take advantage of pygame's collision functions, we needed two to make sure where the collision is coming from
    def collide_x(self, sprite):
        original = self.rect.x
        collision = False
        self.rect.x += self.velocity_x / 2
        if pygame.sprite.collide_mask(self, sprite):
            collision = True
        self.rect.x = original
        return collision

    def collide_y(self, sprite):
        original = self.rect.y
        collision = False
        self.rect.y += self.velocity_y / 2
        if pygame.sprite.collide_mask(self, sprite):
            collision = True
        self.rect.y = original
        return collision

    # Check if ball has hit a line in the player's trail (by a list of points)
    def on_line(self, points):
        for i in xrange(len(points) - 1):
            if min(points[i][0], points[i+1][0]) <= self.rect.left <= max(points[i][0], points[i+1][0]) or \
                        min(points[i][0], points[i+1][0]) <= self.rect.right <= max(points[i][0], points[i+1][0]):
                if abs(self.rect.centery - points[i][1]) < 5:
                    return True
            if min(points[i][1], points[i+1][1]) <= self.rect.top <= max(points[i][1], points[i+1][1]) or \
                        min(points[i][1], points[i+1][1]) <= self.rect.bottom <= max(points[i][1], points[i+1][1]):
                if abs(self.rect.centerx - points[i][0]) < 5:
                    return True
        return False