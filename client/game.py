import asyncio
import logging
import threading

import nest_asyncio
import pygame

# from client_connector import WebSocketClient
from client import client_connector
from client import config as c
from client.client_handler import ClientHandler
from client.state import IPPrompt, PlayGame, StartMenu
from server import server_handler

# connection: Connection = Connection()
# connection = server_connector.main()

nest_asyncio.apply()

pygame.init()

win: pygame.Surface = pygame.display.set_mode((c.W, c.H))
pygame.display.set_caption("The Game :D")
pygame.key.set_repeat(500, 50)

clock: pygame.time.Clock = pygame.time.Clock()

start_menu: StartMenu = StartMenu(win)
ip_prompt: IPPrompt = IPPrompt(win)
game: PlayGame = PlayGame(win)

state_map: dict[str, StartMenu | IPPrompt | PlayGame] = {
    "menu": start_menu,
    "ip": ip_prompt,
    "game": game,
}


def redraw(window: pygame.Surface, game_state: str):
    """Fills the window, calls the appropriate state's redraw function, and updates the window.

    Args:
        window: The window to draw to.
        game_state: The current game state.

    """
    window.fill((255, 255, 255))
    state_map[game_state].redraw()
    pygame.display.flip()


async def main():
    """
    Runs the main game loop.

    game_state needs to be set to game in order for gui to run.
    game_state is temporarily changed to get user_input in order
    to run either server_thread or client_thread.

    server_thread needs to be running before an instance of client_thread
    can connect.

    client_thread can still be run but without server connection.
    """
    game_state: str = "menu"
    websocket = ClientHandler()

    game_running = True
    while game_running:
        events: list[pygame.event.Event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False

        if run_result := await state_map[game_state].update(events, websocket):
            if run_result == "server":
                print(f"user input: {run_result}")

                # sets game_state. game_state needs to be game.
                game_state = "game"

                server_thread = threading.Thread(target=asyncio.run, args=(server_handler.main(),))
                logging.info("Main    : before running server_thread")
                server_thread.start()
                logging.info("Main    : server_thread running.")

                print(server_thread)
                print(type(server_thread))

            elif run_result == "ip":
                print(f"user input: {run_result}")

                # sets game_state. game_state needs to be game.
                game_state = "game"

                # run a client instance with game.
                client_thread = threading.Thread(
                    target=asyncio.run, args=(client_connector.run(),)
                )
                logging.info("Main    : before running client_thread")
                client_thread.start()
                logging.info("Main    : client_thread running.")

            else:
                print(f"run_result: {run_result}")
                game_state = run_result  # make sure game runs.
        redraw(win, game_state)
        await asyncio.sleep(0)
        clock.tick(60)
