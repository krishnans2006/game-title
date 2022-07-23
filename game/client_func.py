"""Websocket client side test script."""

import asyncio

import websockets


async def connect():
    """Websocket client."""
    WS_URL = "ws://127.0.0.1:"
    WS_PORT = "8765"
    URI = f"{WS_URL}{WS_PORT}"

    async with websockets.connect(URI) as websocket:
        client_name = str(websocket.id)
        await websocket.send(client_name)
        print(f"{client_name} connecting to {URI}...")

        while True:
            connected = await websocket.recv()
            print(connected)


if __name__ == "__main__":
    asyncio.run(connect())
