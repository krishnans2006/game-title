import websockets


class Connection:
    """Handles the websocket connection to the running server.

    Attributes:
        host: The IP Address of the server.
        port: The port of the server.
        connection: The websocket connection to the server.

    """

    def __init__(self):
        self.host: str | None = None
        self.port: int | None = None
        self.connection: websockets.WebSocketClientProtocol | None = None

    def connect(self, host: str, port: int) -> None:
        """Connects to the server when the user has provided a host and port.

        Args:
            host: The IP Address to connect to.
            port: The port to connect to.

        """
        self.host = host
        self.port = port
        self.connection = websockets.connect(f"ws://{host}:{port}")
