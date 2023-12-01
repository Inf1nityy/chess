import pygame
import copy
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
            pass

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def number_of_possible_positions(self, depth):
        if depth == 0:
            return 1

        number_of_possible_positions = 0

        for square in self.squares:
            if square.occupying_piece is not None:
                legal_moves = square.occupying_piece.get_legal_moves()
                if legal_moves:
                    for move in legal_moves:
                        # Save the current state of the square and piece
                        previous_position = square.occupying_piece.pos
                        has_moved_previously = square.occupying_piece.has_moved
                        captured_piece = move.occupying_piece

                        # Make the move
                        if square.occupying_piece.move(move):
                            # Recursive call
                            number_of_possible_positions += self.number_of_possible_positions(depth - 1)

                            # Restore the state after the recursive call
                            move.occupying_piece.undo_move(move, square, has_moved_previously, captured_piece)

        return number_of_possible_positions

    def is_in_check(self, color, board_change=None):
        output = False
        king_position = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [i.occupying_piece for i in self.squares if i.occupying_piece is not None]
        if changing_piece is not None:
            if changing_piece.notation == 'k':
                king_position = new_square.pos
        if king_position == None:
            for piece in pieces:
                if piece.notation == 'k' and piece.color == color:
                    king_position = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares():
                    if square.pos == king_position:
                        output = True
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output

    def is_in_checkmate(self, color):
        for square in self.squares:
            if square.occupying_piece != None and square.occupying_piece.color == color:
                if square.occupying_piece.get_legal_moves() != []:
                    return False

        if self.is_in_check(color):
            return True

        return False

