import asyncio
import os
import random
from threading import Thread

import pygame

from client import config as c
from client.client_handler import ClientHandler
from client.gamemechanics.flame_shot import FlameShot
from client.gamemechanics.player import Player
from client.gamemechanics.world import World
from client.state.gamestate import GameState
from client.utility.thread_safe_queue import ThreadSafeQueue


class PlayGame(GameState):
    """A game state that displays the game."""

    move_rate = 8

    def __init__(self, window: pygame.Surface):
        """Initializes the PlayGame game state."""
        super().__init__(window)
        self.name: str = "game"

        self.grass_img = pygame.image.load(os.path.join(os.getcwd()) + "/client/assets/grass.jpg")

        self.main_player: Player = Player(
            random.randint(30, c.TW - 30), random.randint(30, c.TH - 30)
        )

        self.websocket: ClientHandler | None = None

        self.update_thread: Thread = None
        self.thread_cancelled: bool = False

        self.server_response_queue = ThreadSafeQueue()
        self.world = World(self.main_player)

    # TODO:
    def client_payload_dict(self) -> dict:
        """Returns a dict to be passed into the server and received by other players.

        TODO: should send player position (done), orientation, weapon type, events such as
        bullet creation, weapon switching, changes in health, changes
        """
        return self.main_player.to_dict()

    async def update_client(self):
        """Thread that repeatedly updates the websocket connection.

        Sends the current player position to the server, and retrieves the current positions of all
        other players.

        """
        # TODO: timeout error handling, etc.
        await self.websocket.connect()
        while True:
            await asyncio.sleep(0.1)
            if self.thread_cancelled:
                break
            if self.websocket:
                res = await self.websocket.update(self.client_payload_dict())
                self.server_response_queue.append(res)
                print(f"client: received {res}")
            else:
                print("No websocket connection")

        print("\nClient thread cleaning up!\n")

    def stop_thread(self):
        """Stops `update_client` thread. Can be safely called multiple times."""
        self.thread_cancelled = True

    async def update(self, events: list[pygame.event.Event], websocket: ClientHandler):
        """See base class."""
        # region Start client thread
        if not self.websocket:
            self.update_thread = Thread(
                target=asyncio.get_event_loop().run_until_complete,
                args=(self.update_client(),),
            )
            self.websocket = websocket
            self.update_thread.start()
        # endregion

        # region Load new objects into World
        self.world.update(self.server_response_queue)
        # TODO: actually load them once the world's methods are implemented

        # endregion

        for event in events:
            if event.type == pygame.QUIT:
                print("quit")
                await self.cleanup()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: check whether click is left or right
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = mouse_x - c.W // 2, mouse_y - c.H // 2
                print(direction)
                projectile = FlameShot(self.main_player.x, self.main_player.y, direction)
                self.world.spawn_flameshot(projectile)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.main_player.move("left", self.move_rate)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.main_player.move("right", self.move_rate)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.main_player.move("up", self.move_rate)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.main_player.move("down", self.move_rate)

    def redraw(self):
        """See base class."""
        start_x = -((self.main_player.x - c.W // 2) % c.grass_image_width)
        start_y = -((self.main_player.y - c.H // 2) % c.grass_image_height)
        num_x = c.W // c.grass_image_width + 2
        num_y = c.H // c.grass_image_height + 2

        # draw all grass background tiles spaced out c.image_width and c.image_height apart
        for x in range(num_x):
            # and y on screen
            for y in range(num_y):
                self.window.blit(
                    self.grass_img,
                    (start_x + x * c.grass_image_width, start_y + y * c.grass_image_height),
                )
        player_to_right_edge = c.TW - self.main_player.x
        player_to_bottom_edge = c.TH - self.main_player.y
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

        # includes player
        self.world.redraw(self.window)

    async def cleanup(self):
        """Cleans up the websocket connection for the game."""
        self.stop_thread()
        if self.websocket:
            await self.websocket.close()
