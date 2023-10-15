import pygame
import os
from piece import Piece

class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.color = color
        image_path = os.path.join('assets', color[0] + "r.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (board.square_width, board.square_height))
        self.notation = "r"

    def get_legal_moves(self):
        return []
