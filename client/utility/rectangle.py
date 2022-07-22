import pygame


class Rectangle(pygame.Rect):
    def __init__(self, x1, y1, x2, y2, color=(0, 0, 0)):
        super().__init__(x1, y1, x2 - x1, y2 - y1)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
