import math

import pygame

from client.gamemechanics.collidable import Collidable
from client.gamemechanics.gameobject import GameObject


class FlameShot(GameObject, Collidable):
    """A kind of short-range projectile that travels, grows, and sputters out."""

    def __init__(self, x, y, facing: tuple[int, int], no_damage=False) -> None:
        super().__init__(x, y)
        self.no_damage = no_damage
        self.phase = 0
        self._tick = 0
        # the amount of frames between each phase++
        self.animation_delay = 4
        self.maxphase = 8

        # make the hypotenuse of the triangle created by the x and y components of facing equal to 1
        fx, fy = facing
        hyp = math.sqrt(fx**2 + fy**2)
        # ...by dividing the sides of the triangle by the hypotenuse
        fx /= hyp
        fy /= hyp
        self.facing: tuple[float, float] = fx, fy

        self.x = x
        self.y = y

        self._colrect1 = self._rect1(self.x, self.y)
        self._colrect2 = self._rect2(self.x, self.y)
        self._colrect3 = self._rect3(self.x, self.y)

    def phase_tick(self) -> bool:
        """Advances phase of fireball. Returns `True` if final phase (should be destroyed)."""
        self._tick += 1
        if not self._tick % self.animation_delay:
            self.phase += 1
        if self.phase < self.maxphase:
            return False
        return True

    def to_dict(self):
        """See superclass."""
        return {"type": "flameshot", "x": self.x, "y": self.y, "facing": self.facing}

    def _offset(self, multiplier: float) -> tuple[int, int]:
        x = round(self.facing[0] * multiplier)
        y = round(self.facing[1] * multiplier)
        return x, y

    def _draw(self, window: pygame.Surface, rect: pygame.Rect) -> pygame.Rect:
        return pygame.draw.rect(window, (221, 131, 30), rect)

    def _make_rect(self, size, x, y, offset) -> pygame.Rect:
        mx, my = self._offset(offset)
        return pygame.Rect(x + mx, y + my, size, size)

    def _rect1(self, x, y):
        return self._make_rect(40, x - 20, y - 20, 30)

    def _rect2(self, x, y):
        return self._make_rect(70, x - 35, y - 35, 70)

    def _rect3(self, x, y):
        return self._make_rect(106, x - 53, y - 53, 150)

    def draw_at(self, window: pygame.Surface, x: int, y: int):
        """Draw fireball. The center (x, y) is considered to be at the tail, the first Rect."""
        # shorthand for center
        if self.phase < 5:
            self._draw(window, self._rect1(x, y))
        if self.phase >= 1 and self.phase < 6:
            self._draw(window, self._rect2(x, y))
        if self.phase >= 2 and self.phase < 7:
            self._draw(window, self._rect3(x, y))

    # TODO below
    def collidepoint(self, x: int, y: int) -> bool:
        """Check point for collisions with any of the fire rects. Uses absolute coordinates."""
        if self.phase < 5:
            if self._colrect1.collidepoint(x, y):
                return True
        if self.phase >= 1 and self.phase < 6:
            if self._colrect2.collidepoint(x, y):
                return True
        if self.phase >= 2 and self.phase < 7:
            if self._colrect3.collidepoint(x, y):
                return True
        return False

    def colliderect(self, rect: pygame.Rect) -> bool:
        """Check rect for collisions with any of the fire rects. Uses absolute coordinates."""
        if self.phase < 5:
            if self._colrect1.colliderect(rect):
                return True
        if self.phase >= 1 and self.phase < 6:
            if self._colrect2.colliderect(rect):
                return True
        if self.phase >= 2 and self.phase < 7:
            if self._colrect3.colliderect(rect):
                return True
        return False
