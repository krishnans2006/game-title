import string

import pygame


class Cursor:
    def __init__(self, x, y, height):
        self.original_x = x
        self.x = self.original_x
        self.y = y
        self.height = height
        self.show = True
        self.cnt_since_change = 0
        self.change_frames = 15

    def move(self, loc):
        self.x = loc

    def update(self):
        self.cnt_since_change += 1
        if self.cnt_since_change > self.change_frames:
            self.show = not self.show
            self.cnt_since_change = 0

    def draw(self, win):
        if self.show:
            pygame.draw.line(
                win, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height), 2
            )


class TextInput:
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

    def __init__(self, x1, y1, x2, y2, font, maxlength=None):
        self.x = x1
        self.y = y1
        self.width = x2 - x1
        self.height = y2 - y1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = font
        self.maxlength = maxlength
        self.text = ""
        self.disp_text = self.text
        self.text_render = font.render(self.disp_text, 1, (0, 0, 0))
        self.cursor = Cursor(self.x + 5, self.y + 5, self.height - 10)
        self.shift_pressed = False

    def manage_key_press(self, event):
        key_name = pygame.key.name(event.key)
        print(key_name)
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
        self.shift_pressed = False

    def add_key(self, key):
        if self.shift_pressed:
            if key in self.shift_mappings:
                self.text += self.shift_mappings[key]
            else:
                self.text += key.upper()
        else:
            self.text += key
        self.update_cursor_pos()

    def remove_key(self):
        self.text = self.text[:-1]
        self.update_cursor_pos()

    def update_cursor_pos(self):
        if self.maxlength is None or len(self.text) < self.maxlength:
            self.disp_text = self.text
        else:
            self.disp_text = self.text[: self.maxlength]
        self.text_render = self.font.render(self.disp_text, 1, (0, 0, 0))
        if self.text_render.get_width() > self.width - 10:
            self.cursor.move(self.cursor.original_x + self.width - 10)
            self.disp_text = self.disp_text[1:]
        else:
            self.cursor.move(self.cursor.original_x + self.text_render.get_width())

    def update(self):
        self.cursor.update()

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)
        if self.text_render.get_width() > self.width - 10:
            win.blit(
                self.text_render,
                (self.x - (self.text_render.get_width() - self.width + 5), self.y + 5),
            )
        else:
            win.blit(self.text_render, (self.x + 5, self.y + 5))
        self.cursor.draw(win)

    def done(self):
        text = self.text
        self.text = ""
        return text

    def __del__(self):
        del self.cursor
