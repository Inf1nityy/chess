import pygame
import os
from piece import Piece

class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.image_path = os.path.join('assets', color[0] + "r.png")
        self.notation = "r"

    def get_possible_moves(self):
        possible_moves = []
        direction_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for direction_offset in direction_offsets:
            direction_index = 1  # Start from the first square in the direction
            while True:
                target_square_position = (self.pos[0] + direction_index * direction_offset[0], self.pos[1] + direction_index * direction_offset[1])
                target_square = self.board.get_square_from_position(target_square_position)

                if target_square is None:
                    break  # Break if we go out of bounds

                if target_square.occupying_piece is not None:
                    if target_square.occupying_piece.color != self.color:
                        possible_moves.append([target_square])
                    break # Break if we encounter a piece

                possible_moves.append([target_square])

                direction_index += 1  # Move to the next square in the direction

        return possible_moves
