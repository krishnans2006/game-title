from abc import ABC, abstractmethod
from numbers import Number


class GameObject(ABC):
    """An object with coordinates. Can be sent via `to_dict` to the server."""

    def __init__(self, x: Number, y: Number) -> None:
        self.x = x
        self.y = y

    @abstractmethod
    def to_dict():
        """`dict` representation of this GameObject."""
        pass
