import os
import random

import pygame

from client import config as c
from client.state.gamestate import GameState
from client.utility.player import Player
from server.client import WebSocketClient


class PlayGame(GameState):
    """A game state that displays the game."""

    move_rate = 8

    def __init__(self, window: pygame.Surface):
        """Initializes the PlayGame game state."""
        super().__init__(window)
        self.name: str = "game"

        self.grass_img = pygame.image.load(os.path.join(os.getcwd()) + "/client/assets/grass.jpg")

        self.player: Player = Player(random.randint(0, c.TW), random.randint(0, c.TH))

        # TODO: allow port to be edited in UI
        self.websocket_client = WebSocketClient(port=8765)

    def update(self, events: list[pygame.event.Event]):
        """See base class."""
        for event in events:
            if event.type == pygame.QUIT:
                self.websocket_client.cleanup()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move("left", self.move_rate)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move("right", self.move_rate)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move("up", self.move_rate)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move("down", self.move_rate)

        if self.frame_counter == self.correct_frame:
            self.frame_counter = 0
            self.websocket_client.create_message((self.player.to_dict()))

    def redraw(self):
        """See base class."""
        start_x = -((self.player.x - c.W // 2) % c.image_width)
        start_y = -((self.player.y - c.H // 2) % c.image_height)
        num_x = c.W // c.image_width + 2
        num_y = c.H // c.image_height + 2
        for x in range(num_x):
            for y in range(num_y):
                self.window.blit(
                    self.grass_img,
                    (start_x + x * c.image_width, start_y + y * c.image_height),
                )
        player_to_right_edge = c.TW - self.player.x
        player_to_bottom_edge = c.TH - self.player.y
        if player_to_right_edge > c.TW - c.W // 2:
            pygame.draw.rect(
                self.window,
                (255, 0, 0, 127),
                (0, 0, c.W // 2 - (c.TW - player_to_right_edge), c.H),
            )
        if player_to_right_edge < c.W // 2:
            pygame.draw.rect(
                self.window,
                (255, 0, 0, 127),
                (
                    c.W // 2 + player_to_right_edge,
                    0,
                    c.W - (c.W // 2 + player_to_right_edge),
                    c.H,
                ),
            )
        if player_to_bottom_edge > c.TH - c.H // 2:
            pygame.draw.rect(
                self.window,
                (255, 0, 0, 127),
                (0, 0, c.W, c.H // 2 - (c.TH - player_to_bottom_edge)),
            )
        if player_to_bottom_edge < c.H // 2:
            pygame.draw.rect(
                self.window,
                (255, 0, 0, 127),
                (
                    0,
                    c.H // 2 + player_to_bottom_edge,
                    c.W,
                    c.H - (c.H // 2 + player_to_bottom_edge),
                ),
            )
        self.player.redraw(self.window)
