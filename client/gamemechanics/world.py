from typing import List

import pygame

import client.config as c
from client.gamemechanics.flame_shot import FlameShot
from client.gamemechanics.player import Player
from client.utility.thread_safe_queue import ThreadSafeQueue


class World:
    """Manages the objects on the map. Deals with creation, deletion, collisions, etc."""

    def __init__(self, player: Player) -> None:
        self.flameshots: List[FlameShot] = []
        self.players: dict[Player] = []
        # self.bullets:
        self.main_player = player

    def spawn_flameshot(self, obj: FlameShot):
        """Spawn game object."""
        self.flameshots.append(obj)

    def update(self, server_updates: ThreadSafeQueue):
        """Update `main_player` and `objects`. Manages bullet collisions, motion, etc."""
        while update := server_updates.pop():
            self.flameshots = []
            self.players = []
            for player_id, player_data in update.items():
                if player_data["type"] == "player":
                    self.players.append(Player(player_data["x"], player_data["y"], player_id))

        self.flameshots = [fs for fs in self.flameshots if not fs.phase_tick()]

    def absolute_to_relative(self, coord: tuple[int, int]) -> tuple[int, int]:
        """Converts an absolute x, y coordinate to one relative to the top left of the user's screen"""
        x_dist = coord[0] - self.main_player.x + c.W // 2
        y_dist = coord[1] - self.main_player.y + c.H // 2

        return x_dist, y_dist

    def redraw(self, window: pygame.Surface):
        """Draw all game objects, including the player.

        The player is included so that the layering of objects is correct.
        """
        self.main_player.redraw(window)
        for player in self.players:
            # print(self.absolute_to_relative((player.x, player.y)))
            player.draw_at(window, *self.absolute_to_relative((player.x, player.y)))
        for fs in self.flameshots:
            fs.draw_at(window, *self.absolute_to_relative((fs.x, fs.y)))
