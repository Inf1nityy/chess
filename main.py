import pygame
from board import Board
from square import Square
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from rook import Rook
from pawn import Pawn

pygame.init()

if __name__ == "__main__":
    board = Board(800, 800)

    while True:
        board.draw_board()
        pygame.display.update()
