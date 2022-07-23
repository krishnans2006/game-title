import pygame

from client import config as c
from client.state.gamestate import GameState
from client.utility import Rectangle, TextInput


class IPPrompt(GameState):
    """A game state prompting the user for a host and port to connect to a server.

    Attributes:
        host_input: The TextInput object for the host input.
        port_input: The TextInput object for the port input.
        current_focus: The TextInput object that is currently focused.
        submit_button: The Rectangle object for the submit button.
        ip: The IP address provided by the user.

    """

    def __init__(self, window: pygame.Surface):
        """Initializes the IPPrompt game state.

        Args:
            window: The window to draw on.

        """
        super().__init__(window)
        self.name: str = "ip"

        self.host_input: TextInput = TextInput(
            80, 200, 440, 260, c.textbox_font, maxlength=15
        )
        self.port_input: TextInput = TextInput(
            520, 200, 640, 260, c.textbox_font, maxlength=5
        )
        self.current_focus: TextInput | None = None

        self.submit_button: Rectangle = Rectangle(window, 260, 320, 460, 400)

        self.ip: str = ""

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """See base class."""
        for event in events:
            if self.current_focus:
                if event.type == pygame.KEYDOWN:
                    self.current_focus.manage_key_press(event)
                if event.type == pygame.KEYUP and event.key in (
                    pygame.K_RSHIFT,
                    pygame.K_LSHIFT,
                ):
                    self.current_focus.shift_unpressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.submit_button.collidepoint(event.pos):
                    self.ip += self.host_input.text + ":" + self.port_input.text
                    return "game"
                if self.host_input.rect.collidepoint(event.pos):
                    self.current_focus = self.host_input
                    self.host_input.focus()
                    self.port_input.unfocus()
                if self.port_input.rect.collidepoint(event.pos):
                    self.current_focus = self.port_input
                    self.port_input.focus()
                    self.host_input.unfocus()
            if event.type == pygame.MOUSEMOTION:
                if self.submit_button.collidepoint(event.pos):
                    self.submit_button.color = (0, 0, 255)
                else:
                    self.submit_button.color = (0, 0, 0)

    def redraw(self):
        """See base class."""
        text = c.title_font.render("Enter IP:", True, (0, 0, 0))
        self.window.blit(text, (c.W // 2 - text.get_width() // 2, 80))

        self.host_input.draw(self.window)
        text = c.title_font.render(":", True, (0, 0, 0))
        self.window.blit(text, (470, 195))
        self.port_input.draw(self.window)

        self.submit_button.redraw()
        text = c.button_font.render("Submit", True, (255, 255, 255))
        self.window.blit(
            text,
            (
                self.submit_button.x
                + self.submit_button.width // 2
                - text.get_width() // 2,
                self.submit_button.y
                + self.submit_button.height // 2
                - text.get_height() // 2,
            ),
        )
