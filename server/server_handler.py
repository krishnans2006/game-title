"""Websocket server script."""

import asyncio
import base64
import json

import websockets
from data_handler import DataHandler

ACTIVE_CONNECTIONS: set = set()

data_handler: DataHandler = DataHandler()


def store_new_connection(websocket: websockets) -> None:
    """Add new websocket connections to ACTIVE_CONNECTIONS."""
    if websocket.open:
        ACTIVE_CONNECTIONS.add(websocket)
        print(f"Connection from {websocket.id} received.")
    count_active_connections()


def remove_inactive_connection(websocket: websockets) -> None:
    """Remove disconnected websocket connections from ACTIVE_CONNECTIONS."""
    if websocket.closed:
        print(f"ClientHandler {websocket.id} disconnected.")
        ACTIVE_CONNECTIONS.remove(websocket)
        data_handler.remove_player(websocket.id.int)
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


def decode(response: bytes) -> dict:
    """Decode a websocket response into a dictionary.

    Args:
        response: The base64-encoded response from the client.

    """
    return json.loads(base64.b64decode(response).decode())


def encode(dict_obj: dict) -> bytes:
    """Encode a dictionary into a websocket response.

    Args:
        dict_obj: The dictionary to encode as a base64-encoded response.

    """
    return base64.b64encode(json.dumps(dict_obj).encode())


def get_message():
    """Get message."""
    pass


async def connection_handler(
    conn: websockets.WebSocketServerProtocol,
) -> websockets.WebSocketServerProtocol:
    """
    Websocket connection handler.

    Receives:
        "websocket_id"
        "start_game"
        "stop_game"
        "msg"
    """
    try:
        async for recv in conn:

            if conn not in ACTIVE_CONNECTIONS:
                store_new_connection(conn)
            await asyncio.sleep(0.5)
            if conn.open:
                message: dict = decode(recv)
                data_handler.update_player(conn.id.int, message)
                payload: dict = data_handler.get_all_players_but_self(conn.id.int)
                await conn.send(encode(payload))
            else:
                await conn.close()
                remove_inactive_connection(conn)

    except websockets.ConnectionClosed:
        remove_inactive_connection(conn)
        print("ConnectionClosed.")
        pass

    except websockets.ConnectionClosedOK:
        remove_inactive_connection(conn)
        print("ConnectionClosedOK.")
        pass

    except websockets.ConnectionClosedError:
        remove_inactive_connection(conn)
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
        connection_handler, "127.0.0.1", 8765, ping_timeout=5, ping_interval=5
    ):
        print("Websocket server running.")
        count_active_connections()
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.get_event_loop().run_forever()
