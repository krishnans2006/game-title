"""Run server and client scripts."""

import asyncio
import logging
import sys
import threading
import time

import pygame

from client import game  # noqa: F401
from client.client_connector import WebSocketClient  # ugly import statement


def create_client():
    """
    Run an instance of WebSocketClient.

    TODO:
    -   Terminal outputs server_repsonse with an empty dict which will contain relevant data from
        from a call to player.Player.to_dict() -> logic not implementated. Test by running main.py
        on project root.

        player.Player.to_dict() has to be connected to client.client_connector.create_payload() method.

    -   Call to run_game() opens window but only blank / black screen appears.
    """
    ws_client = WebSocketClient()
    asyncio.run(ws_client.establish_connection())


async def run_game():
    """Runs the game instance."""
    await game.main()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"

    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    # server_thread = threading.Thread(target=asyncio.run, args=(server_connector.main(),))
    game_thread = threading.Thread(target=asyncio.run, args=(run_game(),))
    logging.info("Main    : before running game_thread")
    game_thread.start()
    logging.info("Main    : game_thread running.")

    time.sleep(2)  # Wait for server to start.

    # client_thread = threading.Thread(target=create_client())
    # client_thread.start()

    # logging.info("Main    : before running game_thread")
    # game_thread = threading.Thread(
    #     target=asyncio.run, args=(run_game())
    # )  # Opens window but does not run game - blank screen.
    # game_thread.start()

    # logging.info("Main    : wait for the thread to finish")
    # # x.join()
    # logging.info("Main    : all done")

    # asyncio.run(run_game())
