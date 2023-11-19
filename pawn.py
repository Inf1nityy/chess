import pygame
import os
from piece import Piece
from queen import Queen
from knight import Knight
from rook import Rook
from bishop import Bishop

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.color = color
        image_path = os.path.join('assets', color[0] + "p.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (board.square_width, board.square_height))
        self.notation = "p"

    def get_legal_moves(self):
        legal_moves = []
        direction_offset = [-1, 1]

        if self.color == 'white':
            direction_offset.append(-2 if not self.has_moved else 0)
            capture_offset = [(-1, -1), (1, -1)]
        else:
            direction_offset.append(2 if not self.has_moved else 0)
            capture_offset = [(-1, 1), (1, 1)]

        for direction in direction_offset:
            square_position = (self.pos[0], self.pos[1] + direction)
            square = self.board.get_square_from_position(square_position)

            if square is not None:
                if square.occupying_piece is None:
                    legal_moves.append(square)

        for capture in capture_offset:
            square_position = (self.pos[0] + capture[0], self.pos[1] + capture[1])
            if 0 <= square_position[0] < 8:  # Check if the position is on the board
                square = self.board.get_square_from_position(square_position)
                if square is not None:
                    if square.occupying_piece is not None:
                        if square.occupying_piece.color != self.color:
                            legal_moves.append(square)

        return legal_moves

    def check_for_promotion(self):
        if (self.color == "white" and self.pos[1] == 0) or (self.color == "black" and self.pos[1] == 7):
            return True
        return False

    def promote(self, new_piece_type):
        # Assuming new_piece_type is one of "queen", "rook", "bishop", "knight"
        promoted_piece = None

        if new_piece_type == "queen":
            promoted_piece = Queen(self.pos, self.color, self.board)
        elif new_piece_type == "rook":
            promoted_piece = Rook(self.pos, self.color, self.board)
        elif new_piece_type == "bishop":
            promoted_piece = Bishop(self.pos, self.color, self.board)
        elif new_piece_type == "knight":
            promoted_piece = Knight(self.pos, self.color, self.board)

        self.board.get_square_from_position(self.pos).occupying_piece = promoted_piece
