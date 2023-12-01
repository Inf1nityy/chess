import pygame
import sys
from board import Board

pygame.init()
pygame.font.init()
pygame.display.set_caption("Chess")

if __name__ == "__main__":
    board = Board(600, 600)

    #result = board.number_of_possible_positions(depth=1)
    #print(f"Number of possible positions: {result}")

    while True:
        if board.is_in_checkmate('white') or board.is_in_checkmate('black'):
            print("checkmate")
            pygame.quit()
            sys.exit()

        if (board.is_in_stalemate('white') or board.is_in_stalemate('black')) or (board.is_threefold_repetition()) or (board.is_draw_by_fifty_moves()):
            print("draw")
            pygame.quit()
            sys.exit()

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.handle_click(mx, my)

        board.draw_board()
        pygame.display.update()
