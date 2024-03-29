import pygame
import os
from piece import Piece

class Knight(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.image_path = os.path.join('assets', color[0] + "n.png")
        self.notation = "n"

    def get_possible_moves(self):
        possible_moves = []
        direction_offsets = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]

        for direction_offset in direction_offsets:
            target_square_position = (self.pos[0] + direction_offset[0], self.pos[1] + direction_offset[1])
            target_square = self.board.get_square_from_position(target_square_position)

            if target_square is not None and (target_square.occupying_piece is None or target_square.occupying_piece.color != self.color):
                possible_moves.append([target_square])

        return possible_moves
