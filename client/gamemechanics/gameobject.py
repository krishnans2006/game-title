from abc import ABC, abstractmethod
from numbers import Number

import pygame


class GameObject(ABC):
    """An object with coordinates. Can be sent via `to_dict` to the server."""

    def __init__(self, x: Number, y: Number) -> None:
        self.x = x
        self.y = y
        # self.id = _id
        self.visibility_rect: pygame.Rect

    @abstractmethod
    def to_dict(self):
        """`dict` representation of this GameObject."""
        pass

    @abstractmethod
    def draw_at(self, window: pygame.Surface, x: int, y: int):
        """Draws this object on the given window, with the top left corner at the given coordinates."""
        pass
