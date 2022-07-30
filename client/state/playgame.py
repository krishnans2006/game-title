import asyncio
import os
import random
from threading import Thread

import pygame

from client import config as c
from client.client_handler import ClientHandler
from client.state.gamestate import GameState
from client.utility.player import Player


class PlayGame(GameState):
    """A game state that displays the game."""

    move_rate = 8

    def __init__(self, window: pygame.Surface):
        """Initializes the PlayGame game state."""
        super().__init__(window)
        self.name: str = "game"

        self.grass_img = pygame.image.load(os.path.join(os.getcwd()) + "/client/assets/grass.jpg")

        self.player: Player = Player(random.randint(30, c.TW - 30), random.randint(30, c.TH - 30))

        self.websocket: ClientHandler | None = None

        self.update_thread: Thread = None
        self.thread_cancelled = False

    async def update_client(self):
        """Thread that repeatedly updates the websocket connection.

        Sends the current player position to the server, and retrieves the current positions of all
        other players.

        """
        while True:
            await asyncio.sleep(0.5)
            if self.thread_cancelled:
                break
            if self.websocket:
                await self.websocket.update()
            else:
                print("No websocket connection")

        print("\nClient thread cleaning up!\n")

    def stop_thread(self):
        """Stops `update_client` thread. Can be safely called multiple times."""
        self.thread_cancelled = True

    async def update(self, events: list[pygame.event.Event], websocket: ClientHandler):
        """See base class."""
        if not self.websocket:
            self.update_thread = Thread(
                target=asyncio.get_event_loop().run_until_complete,
                args=(self.update_client(),),
            )
            self.update_thread.start()
            await websocket.connect()
            websocket.attach_player(self.player)
            self.websocket = websocket

        for event in events:
            if event.type == pygame.QUIT:
                print("quit")
                await self.cleanup()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move("left", self.move_rate)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move("right", self.move_rate)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move("up", self.move_rate)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move("down", self.move_rate)

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

    async def cleanup(self):
        """Cleans up the websocket connection for the game."""
        self.stop_thread()
        if self.websocket:
            await self.websocket.close()
