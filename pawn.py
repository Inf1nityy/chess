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

        if self.color == 'white':
            direction_offsets = [(0, -1), (-1, -1), (1, -1)]
            if self.has_moved == False:
                direction_offsets.append((0, -2))
        else:
            direction_offsets = [(0, 1), (-1, 1), (1, 1)]
            if self.has_moved == False:
                direction_offsets.append((0, 2))

        for direction_offset in direction_offsets:
            target_square_position = (self.pos[0] + direction_offset[0], self.pos[1] + direction_offset[1])
            target_square = self.board.get_square_from_position(target_square_position)

            if target_square is not None:
                if target_square.occupying_piece is None:
                    if direction_offset[0] * direction_offset[1] == 0:
                        legal_moves.append(target_square)
                else:
                    if target_square.occupying_piece.color != self.color:
                        if direction_offset[0] * direction_offset[1] != 0:
                            legal_moves.append(target_square)

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
