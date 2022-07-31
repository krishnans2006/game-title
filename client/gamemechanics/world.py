from typing import List

import pygame

# from client.gamemechanics.bullet import Bullet
from client.gamemechanics.gameobject import GameObject
from client.gamemechanics.player import Player
from client.utility.thread_safe_queue import ThreadSafeQueue

# from client.utility.thread_safe_queue import ThreadSafeQueue


class World:
    """Manages the objects on the map. Deals with creation, deletion, collisions, etc."""

    def __init__(self, player: Player) -> None:
        self.objects: List[GameObject] = []
        self.players: dict[Player] = []
        # self.bullets:
        self.main_player = player

    def spawn_object(self, obj: GameObject):
        """Spawn game object."""
        self.objects.append(obj)

    def update(self, server_updates: ThreadSafeQueue):
        """Update `main_player` and `objects`. Manages bullet collisions, motion, etc."""
        self.objects = []
        self.players = []
        while update := server_updates.pop():
            for player_id, player_data in update.items():
                if player_data["type"] == "player":
                    self.players.append(Player(player_data["x"], player_data["y"], player_id))

    def absolute_to_relative(self, coord: tuple[int, int]) -> tuple[int, int]:
        """Converts an absolute x, y coordinate to one relative to the top left of the user's screen"""
        x_dist = self.main_player.x - coord[0]
        y_dist = self.main_player.y - coord[1]

        return x_dist, y_dist

    def redraw(self, window: pygame.Surface):
        """Draw all game objects, including the player.

        The player is included so that the layering of objects is correct.
        """
        self.main_player.redraw(window)
        for player in self.players:
            print(self.absolute_to_relative((player.x, player.y)))
            player.draw_at(window, *self.absolute_to_relative((player.x, player.y)))
        for obj in self.objects:
            obj.draw_at(window, *self.absolute_to_relative((obj.x, obj.y)))
