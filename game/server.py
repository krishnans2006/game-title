import asyncio
import json
import websockets

ACTIVE_CONNECTIONS = set()


async def connection_handler(websocket: websockets) -> websockets:
    """
    Websocket connection handler

    TODO:
    - wrong key stored in ACTIVE_CONNECTIONS; new connection being made
    """

    try:
        async for payload in websocket:
            message = json.loads(payload.decode('utf-8'))
            ACTIVE_CONNECTIONS.add(message['websocket_id'])
            print(ACTIVE_CONNECTIONS)
            await websocket.send(f"Received: {payload}")

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {websocket.id} disconnected.")
        ACTIVE_CONNECTIONS.remove(str(websocket.id))


async def main():
    async with websockets.serve(connection_handler, "127.0.0.1", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    if connection_handler:
        print("Websocket server running.")
    asyncio.run(main())
