import pygame
import os
from piece import Piece

class King(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.color = color
        image_path = os.path.join('assets', color[0] + "k.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (board.square_width, board.square_height))
        self.notation = "k"

    def can_castle(self):
        if not self.has_moved:
            if self.color == 'white':
                queenside_rook = self.board.get_piece_from_position((0, 7))
                kingside_rook = self.board.get_piece_from_position((7, 7))

                if queenside_rook != None:
                    if not queenside_rook.has_moved:
                        if [self.board.get_piece_from_position((i, 7)) for i in range(1, 4)] == [None, None, None]:
                            return 'queenside'
                if kingside_rook != None:
                    if not kingside_rook.has_moved:
                        if [self.board.get_piece_from_position((i, 7)) for i in range(5, 7)] == [None, None]:
                            return 'kingside'
            elif self.color == 'black':
                queenside_rook = self.board.get_piece_from_position((0, 0))
                kingside_rook = self.board.get_piece_from_position((0, 7))

                if queenside_rook != None:
                    if not queenside_rook.has_moved:
                        if [self.board.get_piece_from_position((i, 0)) for i in range(1, 4)] == [None, None, None]:
                            return 'queenside'
                if kingside_rook != None:
                    if not kingside_rook.has_moved:
                        if [self.board.get_piece_from_position((i, 0)) for i in range(5, 7)] == [None, None]:
                            return 'kingside'

    def get_possible_moves(self):
        possible_moves = []
        direction_offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for direction_offset in direction_offsets:
            square_position = (self.x + direction_offset[0], self.y + direction_offset[1])

            if (square_position[0] < 8 and square_position[0] >= 0 and square_position[1] < 8 and square_position[1] >= 0):
                possible_moves.append([self.board.get_square_from_position(square_position)])

        return possible_moves

    def get_legal_moves(self):
        legal_moves = []
        for square in self.get_moves():
            if not self.board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                legal_moves.append(square)
        if self.can_castle() == 'queenside':
            legal_moves.append(self.board.get_square_from_position((self.x - 2, self.y)))
        if self.can_castle() == 'kingside':
            legal_moves.append(self.board.get_square_from_position((self.x + 2, self.y)))

        return legal_moves
