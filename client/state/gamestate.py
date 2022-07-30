from abc import ABC, abstractmethod

import pygame

from client.client_handler import ClientHandler


class GameState(ABC):
    """Superclass for all game states.

    Attributes:
        window: The window to draw on.
        name: The name of the game state.

    """

    def __init__(self, window: pygame.Surface):
        """Initializes the game state.

        Args:
            window: The window to draw on.

        """
        self.window: pygame.Surface = window
        self.name: str = ""

    @abstractmethod
    async def update(
        self, events: list[pygame.event.Event], websocket: ClientHandler
    ) -> str | None:
        """Updates the game state

        Args:
            websocket: A Websocket Handler client to use for client server communication.
            events: A list of events from `pygame.event.get()`, used to handle input.

        Returns:
            str if the game state should be changed, None otherwise.

        """
        pass

    @abstractmethod
    def redraw(self):
        """Redraws the elements of the current game state."""
        pass
