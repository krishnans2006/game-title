import pygame

from client import config as c
from client.state.gamestate import GameState
from client.utility import Rectangle


class StartMenu(GameState):
    """A game state displaying the start menu, with options to start a client or server.

    Attributes:
        client_button: The button for starting a client.
        server_button: The button for starting a server.
        settings_icon: The icon for the settings menu.
        settings_rect: The rectangle for the settings icon.

    """

    def __init__(self, window: pygame.Surface):
        """Initializes the StartMenu game state.

        Args:
            window: The window to draw on.

        """
        super().__init__(window)
        self.name: str = "start_menu"

        self.client_button: Rectangle = Rectangle(window, 80, c.H - 160, c.W // 2 - 80, c.H - 80)
        self.server_button: Rectangle = Rectangle(
            window, c.W // 2 + 80, c.H - 160, c.W - 80, c.H - 80
        )

        self.settings_icon: pygame.Surface = pygame.image.load("client/assets/settings.png")
        self.settings_rect: Rectangle = Rectangle.from_rect(
            window,
            self.settings_icon.get_rect(x=c.W - self.settings_icon.get_width() - 20, y=20),
            color=(255, 255, 255),
        )

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """See base class."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.client_button.collidepoint(event.pos):
                    return "ip"
                if self.server_button.collidepoint(event.pos):
                    return "server"
            if event.type == pygame.MOUSEMOTION:
                if self.client_button.collidepoint(event.pos):
                    self.client_button.highlight()
                else:
                    self.client_button.unhighlight()
                if self.server_button.collidepoint(event.pos):
                    self.server_button.highlight()
                else:
                    self.server_button.unhighlight()
                if self.settings_rect.collidepoint(event.pos):
                    self.settings_rect.highlight(color=(200, 200, 200))
                else:
                    self.settings_rect.unhighlight()

    def redraw(self):
        """See base class."""
        text = c.title_font.render("The Game :D", True, (0, 0, 0))
        self.window.blit(text, (c.W // 2 - text.get_width() // 2, 120))

        self.client_button.redraw()
        text = c.button_font.render("Start Client", True, (255, 255, 255))
        self.window.blit(
            text,
            (
                self.client_button.x + self.client_button.width // 2 - text.get_width() // 2,
                self.client_button.y + self.client_button.height // 2 - text.get_height() // 2,
            ),
        )

        self.server_button.redraw()
        text = c.button_font.render("Start Server", True, (255, 255, 255))
        self.window.blit(
            text,
            (
                self.server_button.x + self.server_button.width // 2 - text.get_width() // 2,
                self.server_button.y + self.server_button.height // 2 - text.get_height() // 2,
            ),
        )

        self.settings_rect.redraw()
        self.window.blit(self.settings_icon, self.settings_rect)
