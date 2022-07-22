import sys

import pygame

from client.connection import Connection
from client.utility.rectangle import Rectangle
from client.utility.text_input import TextInput

connection = Connection()

pygame.init()
pygame.font.init()

W = 720
H = 480

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("The Game :D")

clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsans", 30)

client_button = Rectangle(80, 320, 280, 400)
server_button = Rectangle(440, 320, 640, 400)

settings_icon = pygame.image.load("client/assets/settings.png")
settings_rect = settings_icon.get_rect(x=W - settings_icon.get_width() - 20, y=20)

host_input = TextInput(80, 140, 440, 220, font)
port_input = TextInput(520, 140, 640, 220, font)


# MENU


def redraw_menu(window):
    text = font.render("The Game :D", True, (0, 0, 0))
    window.blit(text, (W // 2 - text.get_width() // 2, 120))

    pygame.draw.rect(window, (0, 0, 0), client_button)
    text = font.render("Start Client", True, (255, 255, 255))
    window.blit(
        text,
        (
            client_button.x + client_button.width // 2 - text.get_width() // 2,
            client_button.y + client_button.height // 2 - text.get_height() // 2,
        ),
    )

    pygame.draw.rect(window, (0, 0, 0), server_button)
    text = font.render("Start Server", True, (255, 255, 255))
    window.blit(
        text,
        (
            server_button.x + server_button.width // 2 - text.get_width() // 2,
            server_button.y + server_button.height // 2 - text.get_height() // 2,
        ),
    )

    window.blit(settings_icon, settings_rect)


def run_menu(window, events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if client_button.collidepoint(event.pos):
                return "ip"
            if server_button.collidepoint(event.pos):
                return "server"
        if event.type == pygame.MOUSEMOTION:
            if client_button.collidepoint(event.pos):
                client_button.color = (0, 0, 255)
            else:
                client_button.color = (0, 0, 0)
            if server_button.collidepoint(event.pos):
                server_button.color = (0, 0, 255)
            else:
                server_button.color = (0, 0, 0)
        if event.type == pygame.KEYDOWN:
            host_input.manage_key_press(event)


# IP


def redraw_ip(window):
    text = font.render("Enter IP:", True, (0, 0, 0))
    window.blit(text, (W // 2 - text.get_width() // 2, 80))
    host_input.draw(window)
    port_input.draw(window)


def run_ip(window, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            host_input.manage_key_press(event)
        if event.type == pygame.KEYUP and event.key in (
            pygame.K_RSHIFT,
            pygame.K_LSHIFT,
        ):
            host_input.shift_unpressed()


# SERVER


def redraw_server(window):
    pass


def run_server(window, events):
    # Start server as subprocess
    return "game"  # Switch mode to game


# GAME


def redraw_game(window):
    text = font.render("The Game :D", True, (0, 0, 0))
    window.blit(text, (W // 2 - text.get_width() // 2, 120))


def run_game(window, events):
    pass


# MANAGERS
redraw_map = {
    "menu": redraw_menu,
    "ip": redraw_ip,
    "server": redraw_server,
    "game": redraw_game,
}
run_map = {"menu": run_menu, "ip": run_ip, "server": run_server, "game": run_game}


def redraw(window, game_state):
    window.fill((255, 255, 255))
    redraw_map[game_state](window)
    pygame.display.flip()


def run(window, events, game_state):
    return run_map[game_state](window, events)


def main():
    game_state = "menu"
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if run_result := run(win, events, game_state):
            game_state = run_result  # Change game state
            print(game_state)
        redraw(win, game_state)
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
