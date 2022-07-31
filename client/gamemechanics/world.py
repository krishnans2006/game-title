from typing import List

import pygame

# from client.gamemechanics.bullet import Bullet
from client.gamemechanics.gameobject import GameObject
from client.gamemechanics.player import Player

# from client.utility.thread_safe_queue import ThreadSafeQueue


class World:
    """Manages the objects on the map. Deals with creation, deletion, collisions, etc."""

    def __init__(self) -> None:
        self.objects: List[GameObject] = []

    def set_main_player(self, player: Player):
        """Lets the World know who the main character is.

        Necessary to render objects relative to the main player, who is fixed to the center of the screen.
        """
        self.main_player = player

    def spawn_object(self, obj: GameObject):
        """Spawn game object."""
        self.objects.append(obj)

    def update(self):
        """Update. Manages bullet collisions, etc. TODO"""
        pass

    def redraw(self, window: pygame.Window):
        """Draw all game objects, including the player.

        The player is included so that the layering of objects is correct.
        """
        self.main_player.redraw(window)
        for obj in self.objects:
            obj.redraw()
