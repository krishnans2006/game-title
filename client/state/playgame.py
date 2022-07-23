import pygame

from client import config as c
from client.state.gamestate import GameState


class PlayGame(GameState):
    """A game state that displays the game."""

    def __init__(self, window: pygame.Surface):
        """Initializes the PlayGame game state."""
        super().__init__(window)
        self.name: str = "game"

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """See base class."""
        pass

    def redraw(self):
        """See base class."""
        text = c.button_font.render("The Game :D", True, (0, 0, 0))
        self.window.blit(text, (c.W // 2 - text.get_width() // 2, 120))
