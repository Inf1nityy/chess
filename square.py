import pygame
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from rook import Rook
from pawn import Pawn

class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.coord = self.get_coord()
        self.occupying_piece = None
        self.highlight = False
        self.light_highlight_color = pygame.Color(205, 210, 106)
        self.dark_highlight_color = pygame.Color(170, 162, 58)
        self.highlight_color = self.light_highlight_color if (x + y) % 2 == 0 else self.dark_highlight_color
        self.light_color = pygame.Color(240, 217, 181)
        self.dark_color = pygame.Color(181, 136, 99)
        self.square_color = self.light_color if (x + y) % 2 == 0 else self.dark_color
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def get_coord(self):
        columns = 'abcdefgh'
        return columns[int(self.x)] + str(self.y + 1)

    def draw(self, screen):
        if self.highlight:
            pygame.draw.rect(screen, self.highlight_color, (self.x * self.width, self.y * self.width, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.square_color, (self.x * self.width, self.y * self.width, self.width, self.height))

        if self.occupying_piece != None:
            center_rect = self.occupying_piece.image.get_rect()
            center_rect.center = self.rect.center
            center_rect.x = center_rect.x * self.width
            center_rect.y = center_rect.y * self.height
            screen.blit(self.occupying_piece.image, center_rect.topleft)
