import asyncio
import sys

import pygame

from client import config as c
from client.connection import Connection
from client.state import IPPrompt, PlayGame, StartMenu

connection: Connection = Connection()

pygame.init()

win: pygame.Surface = pygame.display.set_mode((c.W, c.H))

# converts surface from RGB to RGBA -- allows for transparency, fade in/out, etc.
win.convert_alpha()

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


def main():
    """Runs the main game loop."""
    game_state: str = "menu"

    game_running = True
    while game_running:
        events: list[pygame.event.Event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False

        if run_result := state_map[game_state].update(events):
            if run_result == "server":
                # Start server as subprocess
                print("Started server")
                game_state = "game"
            else:
                game_state = run_result  # Change game state
            print(game_state)
        redraw(win, game_state)
        clock.tick(60)


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
    sys.exit()
