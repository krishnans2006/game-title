from typing import Tuple

import pygame

from client.gamemechanics.collidable import Collidable
from client.gamemechanics.gameobject import GameObject


class Bullet(GameObject, Collidable):
    """Bullet GameObject. Shot by players.

    Arguments:
        facing: Tuple[int, int] -- A coordinate relative to the bullet that the bullet would
        eventually reach if it traveled in a straight line.
    """

    def __init__(self, xy: Tuple[int, int], facing: Tuple[int, int]) -> None:
        self.x, self.y = xy

    def collidepoint(self, x: int, y: int) -> bool:
        """See superclass."""
        pass

    def colliderect(self, rect: pygame.Rect) -> bool:
        """See superclass."""
        pass

    def draw_at(self, window: pygame.Surface, x: int, y: int):
        """See superclass."""
        pass
