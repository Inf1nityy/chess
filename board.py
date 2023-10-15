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
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x, y, self.square_width, self.square_height)
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

        # Find the king's position
        for square in self.squares:
            piece = square.occupying_piece
            if piece and piece.notation == "k" and piece.color == color:
                king_position = square.pos
                break

        if king_position is None:
            return False

        # Check if any opponent's piece can move to the king's position
        return any(
            move.pos == king_position
            for square in self.squares
            if square.pos != king_position
            for piece in (square.occupying_piece,)
            if piece and piece.color != color
            for move in piece.get_legal_moves()
        )

    def is_in_checkmate(self, color):
        # 1. Find the king of the specified color
        king = None
        for square in self.squares:
            piece = square.occupying_piece
            if piece and piece.notation == 'k' and piece.color == color:
                king = piece
                break

        if king is None:
            return False  # No king of the specified color found

        # 2. Check if the king is in check
        if self.is_in_check(color):
            # 3. If the king is in check, check if the king has any legal moves to escape check
            for move in king.get_legal_moves():
                # Temporarily move the king to the potential move
                original_square = king.square
                king.square = move
                move.occupying_piece = king

                # Check if the king is still in check after the move
                if not self.is_in_check(color):
                    # The king can escape check, so it's not checkmate
                    king.square = original_square
                    move.occupying_piece = None
                    return False

                # Revert the king's move
                king.square = original_square
                move.occupying_piece = None

            # 4. If there are no legal moves for the king, it's checkmate
            self.get_square_from_position(king.pos).highlight = True
            return True

        return False  # The king is not in check, so it's not checkmate
