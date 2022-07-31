import pygame


class Cursor:
    """Handles the cursor for a TextInput object.

    Attributes:
        original_x: The original x coordinate of the cursor.
        x: The current x coordinate of the cursor.
        y: The current y coordinate of the cursor.
        height: The height of the cursor.
        show: Whether or not the cursor is shown.
        cnt_since_change: The number of frames since the cursor changed.
        change_frames: The number of frames to wait before being hidden.

    """

    change_frames = 30

    def __init__(self, x: int, y: int, height: int):
        """Initializes the cursor.

        Args:
            x: The x coordinate of the cursor.
            y: The y coordinate of the cursor.
            height: The height of the cursor.

        """
        self.original_x: int = x
        self.x: int = self.original_x
        self.y: int = y
        self.height: int = height
        self.show: bool = True
        self.cnt_since_change: int = 0

    def move(self, loc: int):
        """Moves the cursor's horizontal location.

        Args:
            loc: The new location of the cursor.

        """
        self.x = loc

    def update(self):
        """Updates the cursor's visibility.

        If change_frames frames have passed since the cursor changed, it is now changed to either
        hidden or shown.
        """
        self.cnt_since_change += 1
        if self.cnt_since_change > self.change_frames:
            self.show = not self.show
            self.cnt_since_change = 0

    def draw(self, win: pygame.Surface):
        """Draws the cursor to the window as a line.

        Args:
            win: The window to draw the cursor to.

        """
        if self.show:
            pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height), 2)


class TextInput:
    """Creates and handles a textbox.

    Attributes:
        shift_mappings: A dictionary of characters to their shifted versions.
        x: The x coordinate of the textbox.
        y: The y coordinate of the textbox.
        width: The width of the textbox.
        height: The height of the textbox.
        rect: A rectangle for the textbox.
        is_focused: Whether the textbox is focused.
        font: The font to use for text in the textbox.
        maxlength: The maximum number of characters to allow in the textbox.
        text: The current text in the textbox.
        disp_text: a formatted version of text to display in the textbox.
        text_render: A rendered version of disp_text.
        cursor: The cursor for the textbox.
        shift_pressed: Whether the shift key is held down.

    """

    shift_mappings = {
        "`": "~",
        "1": "!",
        "2": "@",
        "3": "#",
        "4": "$",
        "5": "%",
        "6": "^",
        "7": "&",
        "8": "*",
        "9": "(",
        "0": ")",
        "-": "_",
        "=": "+",
        "[": "{",
        "]": "}",
        "\\": "|",
        ";": ":",
        "'": '"',
        ",": "<",
        ".": ">",
        "/": "?",
    }

    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        font: pygame.font.Font,
        maxlength: int = None,
        text: str = "",
    ):
        """Initializes the textbox.

        Args:
            x1: The x coordinate of the top left corner of the textbox.
            y1: The y coordinate of the top left corner of the textbox.
            x2: The x coordinate of the bottom right corner of the textbox.
            y2: The y coordinate of the bottom right corner of the textbox.
            font: The font to use for text in the textbox.
            maxlength: The maximum number of characters to allow in the textbox.

        """
        self.x: int = x1
        self.y: int = y1
        self.width: int = x2 - x1
        self.height: int = y2 - y1
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_focused: bool = False
        self.font: pygame.font.Font = font
        self.maxlength: int = maxlength
        self.text: str = text
        self.disp_text: str = self.text
        self.text_render: pygame.Surface = font.render(self.disp_text, True, (0, 0, 0))
        self.cursor: Cursor = Cursor(self.x + 5, self.y + 5, self.height - 10)
        self.shift_pressed: bool = False

    def focus(self):
        """Focuses the textbox."""
        self.is_focused = True

    def unfocus(self):
        """Unfocuses the textbox."""
        self.is_focused = False

    def manage_key_press(self, event: pygame.event.Event):
        """Handles a key press.

        Adds the key to the textbox if it is a character.
        Handles space, backspace, and shift separately.

        Args:
            event: A pygame.KEYDOWN event.

        """
        key_name = pygame.key.name(event.key)
        if len(key_name) == 1:
            self.add_key(key_name)
            return

        match key_name:
            case "space":
                self.add_key(" ")
            case "backspace":
                self.remove_key()
            case "right shift" | "left shift":
                self.shift_pressed = True

    def shift_unpressed(self):
        """Handles a shift key being released."""
        self.shift_pressed = False

    def add_key(self, key: str):
        """Adds a key to the textbox.

        Args:
            key: The key to add to the textbox.

        """
        if self.shift_pressed:
            if key in self.shift_mappings:
                self.text += self.shift_mappings[key]
            else:
                self.text += key.upper()
        else:
            self.text += key
        self.update_cursor_pos()

    def remove_key(self):
        """Removes the last character from the textbox."""
        self.text = self.text[:-1]
        self.update_cursor_pos()

    def update_cursor_pos(self):
        """Updates the cursor's position based on the textbox's text."""
        if self.maxlength is not None:
            self.text = self.text[: self.maxlength]
        self.disp_text = self.text
        self.text_render = self.font.render(self.disp_text, 1, (0, 0, 0))
        if self.text_render.get_width() > self.width - 10:
            self.cursor.move(self.cursor.original_x + self.width - 10)
            self.disp_text = self.disp_text[1:]
        else:
            self.cursor.move(self.cursor.original_x + self.text_render.get_width())

    def update(self):
        """Updates the cursor."""
        self.cursor.update()

    def draw(self, window: pygame.Surface):
        """Draws the textbox to the window.

        Args:
            window: The window to draw the textbox to.

        """
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        pygame.draw.rect(window, (0, 0, 0), self.rect, 1)
        if self.text_render.get_width() > self.width - 10:
            window.blit(
                self.text_render,
                (
                    self.x - (self.text_render.get_width() - self.width + 10),
                    self.y + self.font.get_ascent() // 4 + 5,
                ),
            )
        else:
            window.blit(
                self.text_render,
                (self.x + 5, self.y + self.font.get_ascent() // 4 + 10),
            )
        if self.is_focused:
            self.cursor.draw(window)

    def done(self):
        """Clears the textbox and returns its text."""
        text = self.text
        self.text = ""
        return text

    def __del__(self):
        """Deletes the textbox's cursor when the textbox is deleted."""
        del self.cursor
