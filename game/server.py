"""Websocket server script."""

import asyncio
import json

import websockets

ACTIVE_CONNECTIONS = set()


def remove_inactive_connection(websocket_id) -> None:
    """Removes disconnected websocket connections from ACTIVE_CONNECTIONS."""
    print(f"Client {websocket_id} disconnected.")
    ACTIVE_CONNECTIONS.remove(websocket_id)
    print(f"Removed {websocket_id}.")


def add_new_connection(websocket_id) -> None:
    """Adds new websocket connections to ACTIVE_CONNECTIONS."""
    ACTIVE_CONNECTIONS.add(websocket_id)
    print(f"Added {websocket_id}.")
    print(f"ACTIVE_CONNECTIONS count: {len(ACTIVE_CONNECTIONS)}")


async def connection_handler(websocket: websockets) -> websockets:
    """Websocket connection handler."""
    try:
        async for payload in websocket:
            message = json.loads(payload.decode('utf-8'))
            websocket_id = message['websocket_id']

            if websocket_id not in ACTIVE_CONNECTIONS:
                add_new_connection(websocket_id)
            await websocket.send(f"Received: {message}")

    except websockets.exceptions.ConnectionClosed:
        remove_inactive_connection(websocket_id)
        pass

    except websockets.exceptions.ConnectionClosedOK:
        remove_inactive_connection(websocket_id)
        pass


async def main():
    """Initialize websocket server."""
    async with websockets.serve(connection_handler, "127.0.0.1", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    if connection_handler:
        print("Websocket server running.")
    asyncio.run(main())
