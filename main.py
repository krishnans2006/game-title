"""Run server and client scripts."""

import asyncio
import sys

import pygame

from client import game


async def run_game():
    """Runs the game instance."""
    await game.main()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(run_game())
