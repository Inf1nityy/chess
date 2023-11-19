import pygame
import os
from piece import Piece

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

            if square.occupying_piece is None:
                legal_moves.append(square)

        for capture in capture_offset:
            square_position = (self.pos[0] + capture[0], self.pos[1] + capture[1])
            if 0 <= square_position[0] < 8:  # Check if the position is on the board
                square = self.board.get_square_from_position(square_position)
                if square.occupying_piece is not None:
                    if square.occupying_piece.color != self.color:
                        legal_moves.append(square)

        return legal_moves
