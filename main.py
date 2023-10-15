import pygame
import sys
from board import Board

pygame.init()
checkmate = False

if __name__ == "__main__":
    board = Board(600, 600)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if checkmate is False:
                    if event.button == 1:
                        board.handle_click(mx, my)

        if board.is_in_checkmate('black'): # If black is in checkmate
            checkmate = True
        elif board.is_in_checkmate('white'): # If white is in checkmate
            checkmate = True

        board.draw_board()
        pygame.display.update()
