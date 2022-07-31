from typing import List

import pygame

# from client.gamemechanics.bullet import Bullet
from client.gamemechanics.gameobject import GameObject
from client.gamemechanics.player import Player

# from client.utility.thread_safe_queue import ThreadSafeQueue


class World:
    """Manages the objects on the map. Deals with creation, deletion, collisions, etc."""

    def __init__(self, player: Player) -> None:
        self.objects: List[GameObject] = []
        self.main_player = player

    def spawn_object(self, obj: GameObject):
        """Spawn game object."""
        self.objects.append(obj)

    def update(self):
        """Update `main_player` and `objects`. Manages bullet collisions, motion, etc. TODO"""
        pass

    def redraw(self, window: pygame.Surface):
        """Draw all game objects, including the player.

        The player is included so that the layering of objects is correct.
        """
        self.main_player.redraw(window)
        for obj in self.objects:
            obj.redraw()
