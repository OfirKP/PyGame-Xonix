# -*- coding: utf-8 -*-
import pygame
from random import randint as rand
from random import  choice
from Ball import Ball
from Polygon import Polygon
from Player import Player
from Button import Menu

pygame.init()   # initializing pygame

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
list_of_colors = [(0, 0, i)for i in xrange(255)] + [(128, 0, j) for j in xrange(50,255, 5)] +\
                 [(0, 128, t) for t in xrange(50, 255, 5)]

# Loading fonts
BIG_FONT = pygame.font.Font("PressStart2P.ttf", 60)
SMALL_FONT = pygame.font.Font("PressStart2P.ttf", 25)
HEART_IMG = pygame.image.load("heart.png")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ARROW_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]  # list of keys

class Game(object):
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.lives = 3
        self.num_of_balls = 2  # Balls on screen
        self.balls = pygame.sprite.Group()  # Group of balls
        self.polygon = Polygon()  # Conquered area
        self.bg_color = choice(list_of_colors)
        self.SURFACE = self.polygon.mask.count()  # Number of conquered pixel after initialization
        self.goal = 60  # Goal percentage of the user (in order to complete the level)
        self.level = 1  # Current level
        self.min_vel = 5  # Minimum velocity
        self.dvel = 2  # Delta of velocity (to create a range of velocities between min and max)
        self.player = Player()


    def percentage(self):  # Calculate percentage of current conquered area
        return float(self.polygon.mask.count() - self.SURFACE)/float(SCREEN_WIDTH*SCREEN_HEIGHT - self.SURFACE)*100

    def is_hit(self):  # Handling events of balls (or the player itself) hitting the player
        if self.player.is_self_destruct():  # the player returned to a location of one of its trails
            return self.lose()
        for ball in self.balls:
            # Check collision of balls with player / its trail
            if ball.alive and ball.on_line(g.player.points) or pygame.sprite.collide_mask(ball, g.player):
                return self.lose()


    def lose(self):  # Reset needed values in order to lose a lide
        self.player = Player()
        self.lives -= 1
        g.player.change_movement(0)
        pygame.time.delay(1000)

    def is_win(self):  # complete a level if the player passed the goal
        return self.percentage() >= self.goal

    def is_over(self):
        return self.lives == 0

    def add_life(self):  # Limit adding lives to 3
        if self.lives <= 2:
            self.lives += 1

    def reset_balls(self):  # Reset balls and randomize their values (in defined range)
        self.balls.empty()
        [self.balls.add(Ball(6, rand(self.min_vel, self.min_vel + self.dvel))) for i in xrange(self.num_of_balls)]
        self.balls.add(Ball(7, self.min_vel + self.dvel, False))

    # Functions that make next levels harder
    def increase_percentage(self):
        self.goal *= 1.05

    def change_velocity(self):
        self.min_vel += 1
        self.dvel += 2
        self.player.speed += 0.5

    def add_ball(self):
        self.num_of_balls += 1

    def lvl_up(self):  # Randomizing a difficulty level from above functions for next levels
        # Display Level Up! text
        text = BIG_FONT.render("Level Up!", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
        self.add_life()  # Give another life (limited to 3)
        pygame.display.flip()
        pygame.time.delay(1500)
        l = [self.add_ball, self.change_velocity, self.increase_percentage]  # List of functions
        self.level += 1
        if self.goal >= 90:  # Don't create goals above 90%
            l.pop()
        f = choice(l)
        f()  # Applying difficulty to next level
        self.polygon = Polygon()
        self.reset_balls()
        self.player = Player()

    def display_hearts(self):  # Displaying current number of lives on screen
        for i in xrange(self.lives):
            screen.blit(HEART_IMG, (10 + 35 * i, SCREEN_HEIGHT - HEART_IMG.get_size()[1] - 10))

    def exit(self):
        pygame.quit()

    def reset(self):  # Initializing values
        self.lives = 3
        self.num_of_balls = 2
        self.balls = pygame.sprite.Group()
        self.polygon = Polygon()
        self.SURFACE = self.polygon.mask.count()
        self.random_color()
        self.goal = 60
        self.level = 1
        self.min_vel = 5
        self.dvel = 2
        self.player = Player()
        self.reset_balls()
        m.show = False  # Close menu


    def resume(self):
        m.show = False

    def random_color(self):
        self.bg_color = choice(list_of_colors)
        self.resume()



try:
    g = Game()
    size = (g.width, g.height)
    screen = pygame.display.set_mode(size)
    HEART_IMG = pygame.transform.scale(HEART_IMG.convert_alpha(), (30, 27))  # creating a smaller heart
    b = False  # boolean for running loop one more time before the next level

    # Menu
    funcs = [(g.exit, "EXIT"), (g.reset, "Reset"), (g.resume, "Resume"), (g.random_color, "Color")]
    m = Menu(funcs)

    g.polygon.update_mask()

    screen.fill(WHITE)
    g.reset_balls()

    # Allowing the user to close the window...
    carryOn = True
    clock = pygame.time.Clock()
    while carryOn:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Handling menu click
                    m.click(pygame.mouse.get_pos())

                elif event.type == pygame.KEYDOWN:
                    if event.key in ARROW_KEYS:
                        old_movement = g.player.movement
                        new_movement = ARROW_KEYS.index(event.key) + 1  # movement in terms of Player class
                        if not g.player.in_conquered:
                            # Player can't go on opposite direction
                            if abs(old_movement - new_movement) == 1 and \
                                (min(old_movement, new_movement) == 1 or min(old_movement, new_movement) == 3):
                                g.lose()
                                break
                            g.player.add_point()  # Add a point to a list of player's trail points
                        g.player.change_movement(new_movement)

                    if event.key == pygame.K_ESCAPE:  # Toggle menu
                        m.show = not m.show

            if not m.show:  # If menu is off
                screen.fill(g.bg_color)
                screen.blit(g.polygon.image, (0, 0))

                # Overlay texts and hearts
                percent_text = SMALL_FONT.render("{0:.1f}".format(g.percentage()) + '%', True, (0, 0, 0))
                level_text = SMALL_FONT.render("Level " + str(g.level), True, (255, 255, 255))
                over_text = BIG_FONT.render("GAME OVER", True, (255, 0, 0))

                screen.blit(percent_text, (SCREEN_WIDTH - percent_text.get_width() - 10,
                                           SCREEN_HEIGHT - percent_text.get_height() - 10))
                screen.blit(level_text, (15, 10))

                g.display_hearts()

                if g.is_over():  # Game over
                    screen.blit(over_text, (SCREEN_WIDTH / 2 - over_text.get_width() / 2,
                                            SCREEN_HEIGHT / 2 - over_text.get_height() / 2))
                    pygame.display.flip()
                    pygame.time.delay(2100)
                    pygame.quit()
                g.is_hit()  # Handle collision with balls / player

                # Updating balls and player and drawing them
                g.balls.update(size, g.polygon)
                g.balls.draw(screen)
                g.player.update(g.polygon, g.balls)

                # Changing last point to player's position and displaying its trail
                if len(g.player.points) > 1:
                    g.player.points[-1] = list(g.player.rect.center)
                    for i in xrange(len(g.player.points) - 1):
                        pygame.draw.line(screen, (255, 0, 0), g.player.points[i], g.player.points[i+1], 3)
                screen.blit(g.player.image, g.player.rect)
            m.show1(screen)

            pygame.display.flip()

            # Running loop one more time before level up (to fill the latest conquered area)
            if b:
                b = False
                g.lvl_up()
            if g.is_win():
                b = True
        except:
            pass
        clock.tick(80)
    pygame.quit()
except:
    pygame.quit()