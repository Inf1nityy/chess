import pygame

class Piece():
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.board = board
        self.color = color
        self.has_moved = False

    def get_valid_moves(self):
        return self.get_legal_moves() + self.get_attacking_moves()

    def move(self, square):
        if square in self.get_valid_moves():
            prev_square = self.board.get_square_from_position(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            square.highlight = True
            self.board.selected_piece = None
            self.has_moved = True

            return True
        else:
            self.board.selected_piece = None
            return False
