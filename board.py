import pygame
from square import Square

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_width = width / 8
        self.square_height = height / 8
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.turn = "white"
        self.selected_piece = None
        self.config = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
        ]
        self.squares = self.generate_squares()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x * self.square_width, y * self.square_height, self.square_width, self.square_height)
                )
        return output

    def draw_board(self):
        for square in self.squares:
            square.draw(self.screen)
