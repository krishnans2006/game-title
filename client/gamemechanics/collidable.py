# TODO: was this a waste?

from abc import ABC, abstractmethod

import pygame


class Collidable(ABC):
    """Inherited by things that have a hitbox."""

    @abstractmethod
    def colliderect(self, rect: pygame.Rect) -> bool:
        """Check if rect collides with this object."""
        return False

    @abstractmethod
    def collidepoint(self, x: int, y: int) -> bool:
        """Check if point collides with this object."""
        return False
