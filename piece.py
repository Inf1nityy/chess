import pygame

class Piece():
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.board = board
        self.color = color
        self.has_moved = False

    def get_moves(self):
        moves = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        moves.append(square)
                        break
                else:
                    moves.append(square)
        return moves

    def get_legal_moves(self):
        return [
            square for square in self.get_moves() 
            if not self.board.is_in_check(self.color, board_change=[self.pos, square.pos])
        ]

    def move(self, square, force=False):
        if square in self.get_legal_moves() and self.color == self.board.turn or force:
            if self.notation == 'p' or square.occupying_piece != None:
                self.board.consecutive_moves = 0
            else:
                self.board.consecutive_moves += 1

            prev_square = self.board.get_square_from_position(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            square.highlight = True
            self.board.selected_piece = None

            if self.notation == "p":
                if self.check_for_promotion():
                    self.promote("queen") # TODO don't hardcode this figure out a way to bring up a menu to let the player pick what they want to promote to

            # Move rook if king castles
            if self.notation == 'k':
                if prev_square.x - self.x == 2:
                    rook = self.board.get_piece_from_position((0, self.y))
                    rook.move(self.board.get_square_from_position((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = self.board.get_piece_from_position((7, self.y))
                    rook.move(self.board.get_square_from_position((5, self.y)), force=True)

            self.has_moved = True

            if force == False:
                self.board.turn = 'white' if self.board.turn == 'black' else 'black'

            return True
        else:
            self.board.selected_piece = None
            return False

    def undo_move(self, current_square, prev_square, has_moved_previously, captured_piece, prev_en_passant_target=None, force=False):
        # Move the piece back to its previous position
        self.pos, self.x, self.y = prev_square.pos, prev_square.x, prev_square.y
        prev_square.occupying_piece = self
        current_square.occupying_piece = captured_piece

        # Unhighlight the square
        current_square.highlight = False
        prev_square.highlight = False

        # Restore previous state
        self.has_moved = has_moved_previously

        # Un-castle the rook if king castled
        if self.notation == 'k' and has_moved_previously is False:
            if prev_square.x - current_square.x == 2:
                rook = self.board.get_square_from_position((3, self.y))
                rook_undo_square = self.board.get_square_from_position((0, self.y))
                rook.occupying_piece.undo_move(rook, rook_undo_square, False, None, force=True)
            elif prev_square.x - current_square.x == -2:
                rook = self.board.get_square_from_position((5, self.y))
                rook_undo_square = self.board.get_square_from_position((7, self.y))
                rook.occupying_piece.undo_move(rook, rook_undo_square, False, None, force=True)


        # Switch the turn back
        if force is False:
            self.board.turn = 'white' if self.board.turn == 'black' else 'black'

    def attacking_squares(self):
        return self.get_moves()
