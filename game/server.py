"""Websocket server script."""

import asyncio
import json

import websockets

ACTIVE_CONNECTIONS = set()


async def connection_handler(websocket: websockets) -> websockets:
    """
    Websocket connection handler.

    TODO:
    - wrong key stored in ACTIVE_CONNECTIONS; new connection being made
    """
    try:
        async for payload in websocket:
            message = json.loads(payload.decode('utf-8'))
            if message['websocket_id'] not in ACTIVE_CONNECTIONS:
                ACTIVE_CONNECTIONS.add(message['websocket_id'])
                print(f"Added {message['websocket_id']}.")
                print(f"ACTIVE_CONNECTIONS count: {len(ACTIVE_CONNECTIONS)}")
            await websocket.send(f"Received: {message}")

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {websocket.id} disconnected.")
        ACTIVE_CONNECTIONS.remove(message['websocket_id'])
        print(f"Removed {websocket.id}.")

        pass
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client {websocket.id} disconnected.")
        pass


async def main():
    """Initialize websocket server."""
    async with websockets.serve(connection_handler, "127.0.0.1", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    if connection_handler:
        print("Websocket server running.")
    asyncio.run(main())
