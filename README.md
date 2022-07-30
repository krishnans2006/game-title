# Welcome to <span style=color:#ca03fc>Plucky Pooka's</span> 2022 Python Discord Code Jam Repository

## About
**`<Game Title>`** is a 2D directional game written in Python. It uses [websockets.io](https://websockets.readthedocs.io/en/stable/) to allow for multiple client connections and [asyncio](https://docs.python.org/3/library/asyncio.html) to handle concurrent functionality.

![](./client/assets/Screenshot_Game_Menu.png)

The game showcases the use of websockets to transmit information back and forth via a `client <--> server <--> client` interaction.

Example output:
```
Websocket server running.
No active connections.
Connection from 0b5f1b13-5bca-418a-8712-8314d85d0796 received.
Active connections: 1
{15115325313996918011285746583835838358: {'x': 1735, 'y': 5697, 'health': 100, 'ping': 250}}
{15115325313996918011285746583835838358: {'x': 1735, 'y': 5697, 'health': 100, 'ping': 250}}
{15115325313996918011285746583835838358: {'x': 1735, 'y': 5697, 'health': 100, 'ping': 250}}
{15115325313996918011285746583835838358: {'x': 1735, 'y': 5697, 'health': 100, 'ping': 250}}
{15115325313996918011285746583835838358: {'x': 1735, 'y': 5697, 'health': 100, 'ping': 250}}
...
...
...
```

## How to Run
*All snippets have to run from within project root directory.*

1. Run `pipenv install -r dev.requirement.txt` to install dependencies.

2. To activate the virtual environment, run ```pipenv shell```.

3. Run the following to start the server: ```python ./server/server_handler.py```.

4. Once the server starts, run the following to start a client: ```python ./client/client_handler.py```.

5. You will be presented with an option to change the ip address of the server. This defaults to `port 8765` on `127.0.0.1` / `localhost`

6. You can use your directional keys to control movement and see data getting transmitted through the active websocket connection.

7. **Enjoy!**

![](./client/assets/Screenshot_Game_Play.png)

## Plucky Pooka Team Members
Krishy Fishy | MyApaulogies | rami.alloush | Pixler | gvsa123

## Future Development
As part of the challenge, we wanted to focus on getting the functionality of the required technologies working before implementing more advanced game-related functionality and features. Below is an outline of what we would like to continue working on:
1. Use ping attacks to slow the movement of another player allowing others to fire more aggressive weapons.
2. Multiplayer LAN functionality
