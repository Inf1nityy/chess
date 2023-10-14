import pygame
import os

class Bishop():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = "w"
        self.dark_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bb.png')), (self.width, self.height))
        self.white_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'wb.png')), (self.width, self.height))
        self.image = self.white_image if self.color == "w" else self.dark_image
        self.image_rect = self.image.get_rect()
