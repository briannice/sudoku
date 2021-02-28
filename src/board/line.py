import pygame

class Line:
    def __init__(self, x, y, width, height, dx, dy):
        self.rect = (x + dx, y + dy, width, height)
        self.color = (0,0,0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)