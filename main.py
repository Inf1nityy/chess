import pygame
import sys
from board import Board

pygame.init()

if __name__ == "__main__":
    board = Board(600, 600)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if board.is_in_checkmate('black') == False and board.is_in_checkmate('white') == False:
                    if event.button == 1:
                        board.handle_click(mx, my)

        board.draw_board()
        pygame.display.update()
