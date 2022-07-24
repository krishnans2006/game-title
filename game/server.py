"""Websocket server script."""

import asyncio
import json

import websockets

ACTIVE_CONNECTIONS = set()


def store_new_connection(websocket: websockets) -> None:
    """Add new websocket connections to ACTIVE_CONNECTIONS."""
    if websocket.open:
        ACTIVE_CONNECTIONS.add(websocket)
        print(f"Connection from {websocket.id} received.")
    count_active_connections()


def remove_inactive_connection(websocket: websockets) -> None:
    """Remove disconnected websocket connections from ACTIVE_CONNECTIONS."""
    if websocket.closed:
        print(f"Client {websocket.id} disconnected.")
        ACTIVE_CONNECTIONS.remove(websocket)
        count_active_connections()


def check_active_connections() -> None:
    """
    Manually check if all stored connections are active.

    TODO:
    - RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    """
    for connection in ACTIVE_CONNECTIONS:
        if connection.open:
            pass
        else:
            remove_inactive_connection(connection)


def count_active_connections() -> None:
    """Return count of all active connections."""
    if len(ACTIVE_CONNECTIONS) > 0:
        print(f"Active connections: {len(ACTIVE_CONNECTIONS)}")
    else:
        print("No active connections.")


def decode_json_payload(payload) -> json:
    """Decode incoming message."""
    return json.loads(payload.decode('utf-8'))


async def connection_handler(websocket: websockets) -> websockets:
    """
    Websocket connection handler.

    Receives:
        "websocket_id"
        "start_game"
        "stop_game"
        "msg"
    """
    try:
        async for _ in websocket:

            if websocket not in ACTIVE_CONNECTIONS:
                store_new_connection(websocket)

            await asyncio.sleep(.5)
            if websocket.open:
                await websocket.send("message['msg']")
            else:
                await websocket.close()
                remove_inactive_connection(websocket)

    except websockets.exceptions.ConnectionClosed:
        remove_inactive_connection(websocket)
        print("ConnectionClosed.")
        pass

    except websockets.exceptions.ConnectionClosedOK:
        remove_inactive_connection(websocket)
        print("ConnectionClosedOK.")
        pass

    except websockets.exceptions.ConnectionClosedError:
        remove_inactive_connection(websocket)
        print("ConnectionClosedError")
        pass

    except asyncio.exceptions.CancelledError:
        print("CancelledError")
        pass

    finally:
        try:
            check_active_connections()
        except RuntimeError:
            check_active_connections()


async def main():
    """Initialize websocket server."""
    async with websockets.serve(
        connection_handler,
        "127.0.0.1",
        8765,
        ping_timeout=5,
        ping_interval=5
    ):
        print("Websocket server running.")
        count_active_connections()
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
