from typing import List

from client.gamemechanics.gameobject import GameObject


class World:
    """Manages the objects on the map. Deals with creation, deletion, collisions, etc."""

    def __init__(self) -> None:
        self.objects: List[GameObject] = []

    def spawn_object(self, obj: GameObject):
        """Spawn game object."""
        pass

    def update(self):
        """Update. Manages bullet collisions, etc. TODO"""
        pass
