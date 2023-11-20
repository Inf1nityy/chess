import pygame
from square import Square
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from rook import Rook
from pawn import Pawn

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_width = width // 8
        self.square_height = height // 8
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.turn = "white"
        self.selected_piece = None
        self.en_passant_target = None
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
        self.setup_board()

    def generate_squares(self):
        output = []
        for file in range(8):
            for rank in reversed(range(8)):
                output.append(
                    Square(file, rank, self.square_width, self.square_height)
                )

        return output

    def get_square_from_position(self, position):
        for square in self.squares:
            if (square.x, square.y) == (position[0], position[1]):
                return square

    def get_piece_from_position(self, position):
        return self.get_square_from_position(position).occupying_piece

    def setup_board(self):
        for y, rank in enumerate(self.config):
            for x, piece in enumerate(rank):
                if piece != '':
                    square = self.get_square_from_position((x, y))
                    if piece[1] == "p":
                        square.occupying_piece = Pawn((x, y), 'white' if piece[0] == 'w' else 'black', self)
                    elif piece[1] == "k":
                        square.occupying_piece = King((x, y), 'white' if piece[0] == 'w' else 'black', self)
                    elif piece[1] == "q":
                        square.occupying_piece = Queen((x, y), 'white' if piece[0] == 'w' else 'black', self)
                    elif piece[1] == "b":
                        square.occupying_piece = Bishop((x, y), 'white' if piece[0] == 'w' else 'black', self)
                    elif piece[1] == "n":
                        square.occupying_piece = Knight((x, y), 'white' if piece[0] == 'w' else 'black', self)
                    elif piece[1] == "r":
                        square.occupying_piece = Rook((x, y), 'white' if piece[0] == 'w' else 'black', self)

    def draw_board(self):
        if self.selected_piece != None:
            for square in self.squares:
                square.highlight = False

            self.get_square_from_position(self.selected_piece.pos).highlight = True

        for square in self.squares:
            square.draw(self.screen)

    def handle_click(self, mx, my):
        x = mx // self.square_width
        y = my // self.square_height
        clicked_square = self.get_square_from_position((x, y))

        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

        elif self.selected_piece.move(clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color):
        king_position = None
        opposite_color = 'black' if color == 'white' else 'white'

        # find the king
        for square in self.squares:
            if square.occupying_piece != None:
                if square.occupying_piece.notation == "k":
                    if square.occupying_piece.color == color:
                        king_position = square.pos

        # check if opponent pieces can capture the king
        for square in self.squares:
            if square.occupying_piece != None:
                if square.occupying_piece.color == opposite_color:
                    for move in square.occupying_piece.get_legal_moves():
                        if move.pos == king_position:
                            return True


        return False

    def is_in_checkmate(self, color):
        return False

