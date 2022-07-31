import math

import pygame

from client.gamemechanics.collidable import Collidable
from client.gamemechanics.gameobject import GameObject


class FlameShot(GameObject, Collidable):
    """A kind of short-range projectile that travels, grows, and sputters out."""

    def __init__(self, x, y, facing: tuple[int, int]) -> None:
        super().__init__(x, y)
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

    def _draw_square(
        self, window: pygame.Surface, size: int, x: int, y: int, offset: int
    ) -> pygame.Rect:
        mx, my = self._offset(offset)
        return pygame.draw.rect(
            window, (221, 131, 30), pygame.Rect(x - size // 2 + mx, y - size // 2 + my, size, size)
        )

    def draw_at(self, window: pygame.Surface, x: int, y: int):
        """Draw fireball. The center (x, y) is considered to be at the tail, the first Rect."""
        # shorthand for center
        if self.phase < 5:
            self._draw_square(window, 40, x, y, 10)
        if self.phase > 0 and self.phase < 6:
            self._draw_square(window, 70, x, y, 50)
        if self.phase > 1 and self.phase < 7:
            self._draw_square(window, 105, x, y, 130)

        # if self.phase > 1 and self.phase < 8:
        #     pygame.draw.rect(
        #         window,
        #         (221, 131, 30),
        #         pygame.Rect(x - 10, y - 10, 20, 20)
        #     )

    # TODO below
    def collidepoint(self, x: int, y: int) -> bool:
        """Check point for collisions with any of the fire rects."""
        return super().collidepoint(x, y)

    def colliderect(self, rect: pygame.Rect) -> bool:
        """Check rect for collisions with any of the fire rects."""
        return super().colliderect(rect)
