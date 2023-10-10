import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

def draw_board():
    for file in range(8):
        for rank in range(8):
            is_light_square = (file + rank) % 2 != 0;
            light_color = pygame.Color(240, 217, 181)
            dark_color = pygame.Color(181, 136, 99)
            square_color = None

            if is_light_square:
                square_color = light_color
            else:
                square_color = dark_color


            pygame.draw.rect(screen, square_color, (file * 100, rank * 100, 100, 100))

while True:
    draw_board()
    pygame.display.update()
