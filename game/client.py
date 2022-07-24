"""Websocket Client side script."""

import asyncio
import json
import random
from typing import Dict

import websockets


class WebSocketClient():
    """Websocket client."""

    def __init__(self) -> None:
        """Initialize class with url variables."""
        self.ws_url: str = "ws://127.0.0.1:"
        self.ws_port: int = 8765
        self.uri = f"{self.ws_url}{self.ws_port}"
        self.delay = 1

    def create_payload(self, WEBSOCKET_ID: str, MESSAGE: str) -> Dict:
        """Construct payload."""
        payload = {
            "websocket_id": WEBSOCKET_ID,
            "start_game": True,
            "stop_game": False,
            "msg": MESSAGE
        }

        return json.dumps(payload).encode('utf-8')

    def create_message(self) -> str:
        """Create a message to be included in payload."""
        return random.randint(1, 5)

    async def establish_connection(self) -> None:
        """Establish connection to server."""
        try:
            async with websockets.connect(self.uri) as websocket:
                WEBSOCKET_ID = str(websocket.id)
                print(f"Client {websocket.id} connected.")

                while True:
                    await websocket.send(self.create_payload(
                        WEBSOCKET_ID,
                        MESSAGE=self.create_message()
                    ))
                    await asyncio.sleep(self.delay)
                    _ = await websocket.recv()
                    print(_)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Error: {e}.")

        finally:
            await websocket.close()


client = WebSocketClient()
asyncio.run(client.establish_connection())
