import pygame
from square import Square

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

squares = []

def initialize_board():
    for file in range(8):
        for rank in range(8):
            square = Square(file * 100, rank * 100)
            squares.append(square)

initialize_board()

while True:
    for square in squares:
        square.draw(screen)
    pygame.display.update()
