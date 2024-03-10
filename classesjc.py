import pygame

BOMB_IMG = None
CROISSANT_IMG = None
LASER_IMG = None


def load_images():
    global BOMB_IMG, CROISSANT_IMG, LASER_IMG
    pygame.init()
    BOMB_IMG = pygame.image.load("media/art/Bomb.png").convert()
    BOMB_IMG.set_colorkey((255, 0, 0))
    CROISSANT_IMG = pygame.image.load("media/art/Croissant.png").convert()
    CROISSANT_IMG.set_colorkey((255, 0, 0))
    LASER_IMG = pygame.image.load("media/art/Laser.png").convert()
    LASER_IMG.set_colorkey((255, 255, 255))


class Bomb():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, DISPLAY):
        DISPLAY.blit(BOMB_IMG, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x + 1, self.y + 1, 15, 15)

    def collision_test(self, player):
        Bomb_rect = self.get_rect()
        return Bomb_rect.colliderect(player)

    def move(self):
        self.y += 2


class Croissant():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, DISPLAY):
        DISPLAY.blit(CROISSANT_IMG, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

    def collision_test(self, player):
        Croissant_Rect = self.get_rect()
        return Croissant_Rect.colliderect(player)


class Laser():
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def render(self, DISPLAY):
        DISPLAY.blit(LASER_IMG, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 10, 1)

    def collision_test(self, player):
        Laser_Rect = self.get_rect()
        return Laser_Rect.colliderect(player)

    def move(self):
        if self.dir == 'left':
            self.x += 3
        else:
            self.x -= 3