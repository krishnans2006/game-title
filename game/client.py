from typing import Dict

import asyncio
import json
import websockets


class WebSocketClient():
    """Websocket client"""
    def __init__(self) -> None:
        self.ws_url: str = "ws://127.0.0.1:"
        self.ws_port: int = 8765
        self.uri = f"{self.ws_url}{self.ws_port}"

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
        """Create a message to be included in payload"""
        return input("Please enter your message: ")

    async def establish_connection(self) -> None:
        """
        Connect to server

        TODO:
        - issue with keep-alive; where to send ping?
        """
        try:
            async with websockets.connect(self.uri) as websocket:

                while True:
                    print(f"Client {websocket.id} connected.")
                    WEBSOCKET_ID = str(websocket.id)
                    await websocket.send(self.create_payload(WEBSOCKET_ID, MESSAGE=self.create_message()))

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Error: {e}.")

        finally:
            _ = await websocket.recv()
            print(_)


client = WebSocketClient()
asyncio.run(client.establish_connection())
