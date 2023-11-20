import pygame

class Piece():
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.board = board
        self.color = color
        self.has_moved = False

    def move(self, square):
        if square in self.get_legal_moves():
            prev_square = self.board.get_square_from_position(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            square.highlight = True
            self.board.selected_piece = None

            if self.notation == "p":
                if self.has_moved == False:
                    if abs(prev_square.y - square.y) == 2:
                        self.board.en_passant_target = self

                if self.check_for_promotion():
                    self.promote("queen") # TODO don't hardcode this figure out a way to bring up a menu to let the player pick what they want to promote to

            self.has_moved = True

            if self.board.en_passant_target != None:
                if self.board.en_passant_target.color != self.color:
                    self.board.en_passant_target = None

            return True
        else:
            self.board.selected_piece = None
            return False
