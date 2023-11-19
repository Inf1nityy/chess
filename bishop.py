import pygame
import os
from piece import Piece

class Bishop(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.color = color
        image_path = os.path.join('assets', color[0] + "b.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (board.square_width, board.square_height))
        self.notation = "b"

    def get_legal_moves(self):
        legal_moves = []
        direction_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for direction_offset in direction_offsets:
            for direction_index in range(8):
                target_square_position = (self.pos[0] + direction_index * direction_offset[0], self.pos[1] + direction_index * direction_offset[1])
                target_square = self.board.get_square_from_position(target_square_position)

                if target_square == None:
                    break

                if target_square.occupying_piece is not None:
                    print(self.board.squares[0].coord)
                    print(self.board.squares[0].pos)
                    print(target_square.coord)
                    print(target_square.occupying_piece.color)

                legal_moves.append(target_square)

        return legal_moves
