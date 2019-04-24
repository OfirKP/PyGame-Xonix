import pygame

pygame.font.init()

#  Constants
BABY_BLUE = (94, 157, 200)
DARK_BLUE = (12, 44, 82)
SMALL_FONT = pygame.font.Font("PressStart2P.ttf", 25)
GRAY = (102, 102, 102)


class Button(object):
    def __init__(self, func=None, text="", pos=(25, 25), width=200, height=80):
        self.function = func
        self.text = text
        self.rect = pygame.Rect(pos, (width, height))



    def show(self, surface):
        pygame.draw.rect(surface, BABY_BLUE, self.rect)
        pygame.draw.rect(surface, DARK_BLUE, self.rect, 4)
        label = SMALL_FONT.render(self.text, True, (0, 0, 0))
        surface.blit(label, (self.rect.centerx - label.get_width()/2, self.rect.centery - label.get_height()/2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        self.function()


class Menu(object):
    def __init__(self, buttons=[], width=300):
        pos = [20, 10]
        self.top_left = (20, 20)
        self.size = (width, len(buttons)*90 + 20)
        self.screen = pygame.Surface(self.size)
        self.screen.fill(GRAY)
        self.show = False
        self.buttons = []
        for func in buttons:
            self.buttons.append(Button(func[0], func[1], pos, self.size[0]-40, 80))
            pos[1] += 80 + 10

    def show1(self, surface):  # show menu
        if self.show:
            for b in self.buttons:
                b.show(self.screen)
            surface.blit(self.screen, self.top_left)

    def click(self, pos):
        pos_temp = (pos[0] - self.top_left[0], pos[1] - self.top_left[1])
        if self.show:
            for b in self.buttons:
                if b.is_clicked(pos_temp):
                    b.click()
