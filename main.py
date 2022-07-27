"""Run server and client scripts."""

import asyncio
import logging
import sys
import threading
import time

import pygame

from client import game  # noqa: F401
from client.client import WebSocketClient  # ugly import statement
from server import server


def create_client():
    """Run an instance of WebSocketClient."""
    ws_client = WebSocketClient()
    asyncio.run(ws_client.establish_connection())


def run_game():
    """Runs the game instance."""
    game.main()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"

    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    logging.info("Main    : before running thread")
    server_thread = threading.Thread(
        target=asyncio.run, args=(server.main(),)
    )  # process is blocking next thread.
    server_thread.start()
    time.sleep(2)
    client_thread = threading.Thread(target=create_client())
    client_thread.start()

    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")
