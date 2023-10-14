import pygame

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.coord = self.get_coord()
        self.light_color = pygame.Color(240, 217, 181)
        self.dark_color = pygame.Color(181, 136, 99)
        self.square_color = self.light_color if (x / 100 + y / 100) % 2 == 0 else self.dark_color

    def get_coord(self):
        columns = 'abcdefgh'
        return columns[int(self.x / 100)] + str(int(self.y / 100) + 1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.square_color, (self.x, self.y, self.width, self.height))
