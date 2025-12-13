from __future__ import annotations
from . import load_file, save_file
from typing import TYPE_CHECKING
from .models.player import Player

if TYPE_CHECKING:
    from rcon_monitor import RconMonitor


class Status:
    """Tracks player join/leave events and notification state."""

    def __init__(self, monitor: RconMonitor, path=None):

        self.monitor = monitor

        self.players: dict[str, Player] = {}  # {player_name: Player}
        self.notify = 0     # flag for whether a notification should be sent
        self.message = ""   # accumulated join/leave messages
        self.path = path

        self.load()

    def player_manager(self, players: list[str]) -> dict[str, Player]:
        player_dict = {}
        for pname in players:
            player_dict[pname] = Player(username=pname)
        return player_dict

    def update_player_status(self):
        current_players = self.monitor.snapshot.player_names
        tracked = self.players
        notify_flag = 0
        message_log = ""

        # join/leave logic
        for player_name in current_players:
            if player_name not in tracked or tracked[player_name].status in ("offline", "left"):
                player = tracked.get(player_name) or Player(
                    username=player_name)
                player.update_status("joined")
                tracked[player_name] = player
                notify_flag = 1
                message_log += f"{player_name} has joined the server!\n"
            elif tracked[player_name].status == "joined":
                tracked[player_name].status = "online"

        for player in list(tracked.values()):
            if player.username not in current_players:
                if player.status == "online":
                    player.update_status("left")
                    notify_flag = 1
                    message_log += f"{player.username} has left the server.\n"
                elif player.status == "left":
                    player.update_status("offline")
                elif player.status == "joined":
                    player.update_status("left")
                    notify_flag = 1
                    message_log += f"{player.username} has left the server.\n"

            tracked[player.username] = player

        self.players = tracked
        self.notify = notify_flag
        self.message = message_log.strip()

        if notify_flag and message_log:
            self.monitor.send_ntfy(self.message)

        self.save()

        return self

    def to_dict(self):
        return {
            "players": {player.username: player.to_dict() for player in self.players.values()},
            "notify": self.notify,
            "message": self.message,
        }

    def reset(self):
        self.notify = 0
        self.message = ""

    def load(self):
        if self.path:
            loaded = load_file(self.path, {"players": {}})
            player_names = list(loaded["players"].keys())
            self.players = self.player_manager(player_names)
            self.notify = loaded.get("notify", 0)
            self.message = loaded.get("message", "")

    def save(self):
        """Save snapshot to its path as JSON."""
        if self.path:
            save_file(self.path, self.to_dict())
