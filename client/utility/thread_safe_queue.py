from threading import Lock
from typing import Any


class ThreadSafeQueue:
    """Thread-safe queue."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._contents = []

    def append(self, obj: Any):
        """Append element to end of queue."""
        with self._lock:
            self._contents.append(obj)

    def pop(self) -> Any:
        """Remove and return oldest element. If empty, return None."""
        with self._lock:
            if self._contents:
                return self._contents.pop(0)
            return None

    def peek(self) -> Any:
        """Look at oldest element. If empty, return None."""
        with self._lock:
            if self._contents:
                return self._contents[0]
            return None
