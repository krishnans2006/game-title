import pygame

from client import config as c
from client.gamemechanics.collidable import Collidable
from client.gamemechanics.gameobject import GameObject
from client.utility import Rectangle


class Player(GameObject, Collidable):
    """Handles a Player in the game.

    Attributes:
        x: The current x coordinate of the player.
        y: The current y coordinate of the player.
        width: The width of the player icon.
        height: The height of the player icon.
        health: The current health of the player.
        gun: The gun the player is holding (to be implemented).
        ping: The current ping value of the player.

    """

    def __init__(self, x: int, y: int, name: str = "Player1"):
        super().__init__(x, y)
        """Initializes the player.

        Args:
            x: The starting x coordinate of the player.
            y: The starting y coordinate of the player.

        """
        self.x: int = x
        self.y: int = y
        self.width: int = 60
        self.height: int = 60
        self.hitbox_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name: str = name

        self.health: int = 100
        self.gun: None = None
        self.ping: int = 250

    def move(self, direction: str, distance: int):
        """Moves the player in the given direction by the given distance.

        Args:
            direction: The direction to move the player in.
            distance: The distance to move the player in pixels.

        """
        if direction == "up":
            self.y -= distance
        elif direction == "down":
            self.y += distance
        elif direction == "left":
            self.x -= distance
        elif direction == "right":
            self.x += distance

        if self.x - self.width // 2 < 0:
            self.x = 0 + self.width // 2
        if self.y - self.height // 2 < 0:
            self.y = 0 + self.height // 2
        if self.x + self.height // 2 > c.TW:
            self.x = c.TW - self.height // 2
        if self.y + self.height // 2 > c.TH:
            self.y = c.TH - self.height // 2

    # maybe todo: just call self.draw_at(0, 0) ?
    def redraw(self, window: pygame.Surface):
        """Redraws the player on the given window.

        Args:
            window: The window to draw the player on.

        """
        pygame.draw.rect(
            window,
            (0, 0, 0),
            (
                c.W // 2 - self.width // 2,
                c.H // 2 - self.height // 2,
                self.width,
                self.height,
            ),
        )

        text = c.text_font.render(f"{self.ping}ms", True, (255, 255, 255))
        Rectangle.draw_rect_alpha(
            window,
            (0, 0, 0, 120),
            (
                c.W // 2 - text.get_width() // 2 - 2,
                c.H // 2 - self.height // 2 - text.get_height() - 8,
                text.get_width() + 4,
                text.get_height() + 4,
            ),
        )
        window.blit(
            text,
            (
                c.W // 2 - text.get_width() // 2,
                c.H // 2 - self.height // 2 - text.get_height() - 5,
            ),
        )

        pygame.draw.rect(
            window,
            (0, 0, 0),
            (
                c.W // 2 - self.width // 2,
                c.H // 2 + self.height // 2 + 3,
                self.width,
                20,
            ),
        )
        scale_factor = self.width - 6
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                c.W // 2 - self.width // 2 + 3,
                c.H // 2 + self.height // 2 + 6,
                scale_factor,
                14,
            ),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                c.W // 2 - self.width // 2 + 3,
                c.H // 2 + self.height // 2 + 6,
                scale_factor * (self.health / 100),
                14,
            ),
        )

    def draw_at(self, window: pygame.Surface, x: int, y: int):
        """Draws relative to top left of screen."""
        pygame.draw.rect(
            window,
            (0, 0, 0),
            (
                x - self.width // 2,
                y - self.height // 2,
                self.width,
                self.height,
            ),
        )

        text = c.text_font.render(f"{self.ping}ms", True, (255, 255, 255))
        Rectangle.draw_rect_alpha(
            window,
            (0, 0, 0, 120),
            (
                c.W // 2 - text.get_width() // 2 - 2,
                c.H // 2 - self.height // 2 - text.get_height() - 8,
                text.get_width() + 4,
                text.get_height() + 4,
            ),
        )
        window.blit(
            text,
            (
                c.W // 2 - text.get_width() // 2,
                c.H // 2 - self.height // 2 - text.get_height() - 5,
            ),
        )

        pygame.draw.rect(
            window,
            (0, 0, 0),
            (
                c.W // 2 - self.width // 2,
                c.H // 2 + self.height // 2 + 3,
                self.width,
                20,
            ),
        )
        scale_factor = self.width - 6
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                c.W // 2 - self.width // 2 + 3,
                c.H // 2 + self.height // 2 + 6,
                scale_factor,
                14,
            ),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                c.W // 2 - self.width // 2 + 3,
                c.H // 2 + self.height // 2 + 6,
                scale_factor * (self.health / 100),
                14,
            ),
        )

    def to_dict(self):
        """Returns a dictionary representation of the player for easy transmission."""
        return {
            "type": "player",
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "ping": self.ping,
        }

    def collidepoint(self, x: int, y: int) -> bool:
        """See superclass."""
        return self.hitbox_rect.collidepoint(x, y)

    def colliderect(self, rect: pygame.Rect) -> bool:
        """See superclass."""
        return self.hitbox_rect.colliderect(rect)
