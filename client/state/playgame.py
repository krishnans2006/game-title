import pygame

from client import config as c
from client.state.gamestate import GameState
from client.utility import Rectangle


class PlayGame(GameState):
    """A game state that displays the game."""

    move_rate = 5

    def __init__(self, window: pygame.Surface):
        """Initializes the PlayGame game state."""
        super().__init__(window)
        self.name: str = "game"

        self.player: Rectangle = Rectangle(window, 150, 90, 210, 150, (255, 0, 0))

        self.quadrants: list[Rectangle] = [
            Rectangle(window, 0, 0, c.W // 2, c.H // 2, (50, 50, 50)),  # top left
            Rectangle(window, c.W // 2, 0, c.W, c.H // 2, (100, 100, 100)),  # top right
            Rectangle(
                window, 0, c.H // 2, c.W // 2, c.H, (200, 200, 200)
            ),  # bottom left
            Rectangle(
                window, c.W // 2, c.H // 2, c.W, c.H, (150, 150, 150)
            ),  # bottom right
        ]
        self.current_quadrant: int = 0
        self.quadrants[self.current_quadrant].highlight()

    def update(self, events: list[pygame.event.Event]):
        """See base class."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move("left", self.move_rate)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move("right", self.move_rate)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move("up", self.move_rate)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move("down", self.move_rate)
        for i, quadrant in [
            (i, q) for i, q in enumerate(self.quadrants) if i != self.current_quadrant
        ]:
            if quadrant.contains(self.player):
                self.quadrants[i].highlight()
                self.quadrants[self.current_quadrant].unhighlight()
                self.current_quadrant = i
                break

    def redraw(self):
        """See base class."""
        for quadrant in self.quadrants:
            quadrant.redraw()
        self.player.redraw()
