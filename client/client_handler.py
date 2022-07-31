"""Websocket ClientHandler side script."""

import base64
import json

import websockets


def decode(response: bytes) -> dict:
    """Decode a websocket response into a dictionary.

    Args:
        response: The base64-encoded response from the server.

    """
    return json.loads(base64.b64decode(response).decode())


def encode(dict_obj: dict) -> bytes:
    """Encode a dictionary into a websocket response.

    Args:
        dict_obj: The dictionary to encode as a base64-encoded response.

    """
    return base64.b64encode(json.dumps(dict_obj).encode())


class ClientHandler:
    """Websocket client."""

    def __init__(self) -> None:
        """Initializes the class with url variables."""
        self.ws_url: str = "127.0.0.1"
        self.ws_port: int = 8765
        self.uri = f"{self.ws_url}:{self.ws_port}"

        self.connection = self.connection_thread = None

    def setup(self, url: str = "127.0.0.1", port: int = 8765) -> None:
        """Sets up the class with url variables."""
        self.ws_url = url
        self.ws_port = port
        self.uri = f"ws://{self.ws_url}:{self.ws_port}"

    async def connect(self):
        """Initiates the connection to the server."""
        self.connection = await websockets.connect(self.uri)

    async def update(self, to_send: dict) -> dict:
        """Updates the server with client data and the client with server data.

        The server receives the latest player information from the client, and send back the latest
        information about other players.

        """
        await self.connection.send(encode(to_send))
        server_response: dict = decode(await self.connection.recv())
        # print(f"Server response: {server_response}")
        return server_response

    async def close(self):
        """Closes the websocket connection."""
        await self.connection.close()
