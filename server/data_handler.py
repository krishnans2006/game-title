from typing import Any


class DataHandler:
    """Handles player data for the server, which is constantly updated by client handlers.

    Attributes:
        players: A dictionary of player data, mapping a player id to the most recent data retrieved
        from the player.

    """

    def __init__(self):
        """Initializes the data handler."""
        self.players: dict[int, dict[str, Any]] = {}

    def update_player(self, player_id: int, player_data: dict):
        """Updates the player data for the given player id

        Called when a client sends updated data to the server.

        Args:
            player_id: The id of the player to update, the integer value of the uuid.
            player_data: The data to update the player with, including position, health, and ping.

        """
        self.players[player_id] = player_data

    def get_player(self, player_id: int):
        """Returns the player data for the given player id.

        Args:
            player_id: The id of the player to get data for, the integer value of the uuiid.

        """
        return self.players.get(player_id)

    def remove_player(self, player_id: int):
        """Removes the player from the data handler. Called when a client disconnects.

        Args:
            player_id: The id of the player to remove, the integer value of the uuid.

        """
        del self.players[player_id]

    def get_all_players_but_self(self, player_id: int):
        """Returns all player data except for the given player id.

        Args:
            player_id: The id of the player to exclude, the integer value of the uuid.

        """
        return {id_: player for id_, player in self.players.items() if id_ != player_id}
