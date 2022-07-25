"""Run server and client scripts."""

import asyncio
import logging
import os
import threading
import time

from game.client import WebSocketClient


def run_server():
    """Run the websocket server script."""
    try:
        cwd = [os.getcwd().split('/')]

        if cwd == 'plucky-pooka-cj22':
            os.system('python ./game/server.py')
        elif cwd == 'bug':
            os.system('python ~/plucky-pooka-cj22/game/server.py')
    except Exception:
        print(f"Please run inside project directory. Current directory: {cwd}.")


def create_client():
    """Run an instance of WebSocketClient."""
    ws_client = WebSocketClient()
    asyncio.run(ws_client.establish_connection())


if __name__ == "__main__":
    cwd = [os.getcwd().split('/')]

    if cwd == 'plucky-pooka-cj22':
        os.chdir('../game')

    print(cwd[-1])
    print(os.getcwd())

    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,
    #                     datefmt="%H:%M:%S")

    # logging.info("Main    : before creating thread")

    # ws_srv = threading.Thread(target=run_server)
    # ws_clt = threading.Thread(target=create_client)

    # logging.info("Main    : before running thread")

    # ws_srv.start()
    # while not ws_srv.is_alive():
    #     time.sleep(2)

    # # print(dir(ws_srv))
    # # threading.Condition.wait_for(ws_srv.is_alive(), timeout=20)
    # # threading.Condition.notify_all()
    # ws_clt.start()

    # logging.info("Main    : wait for the thread to finish")
    # # x.join()
    # logging.info("Main    : all done")
