from __future__ import annotations
import re
from typing import TYPE_CHECKING

from monitor.models.version import Version

if TYPE_CHECKING:
    from rcon_monitor import RconMonitor


class Commander:
    def __init__(self, monitor: RconMonitor):
        self.monitor = monitor

    def send_command(self, command: str) -> str:
        return self.monitor.send_command(command)

    def broadcast_message(self, message: str):
        command = f'say {message}'
        return self.send_command(command)

    def get_player_data(self):
        response = self.monitor.send_command('list')
        match = re.search(
            r"There are (\d+) of a max of (\d+) players online", response)
        player_count, max_players, players = 0, 0, []
        if match:
            player_count, max_players = int(
                match.group(1)), int(match.group(2))
        if ":" in response:
            players_str = response.split(":", 1)[1].strip()
            if players_str:
                players = [p.strip()
                           for p in players_str.split(",") if p.strip()]
        return {"player_count": player_count, "max_players": max_players, "players": players}

    def get_daytime_ticks(self):
        """Get current daytime ticks from server."""
        response = self.send_command("time query daytime")
        match = re.search(r"The time is (\d+)", response)
        if match:
            return int(match.group(1))
        raise ValueError("Could not parse daytime ticks from response.")

    def get_game_ticks(self):
        """Get current game ticks from server."""
        response = self.send_command("time query gametime")
        match = re.search(r"The time is (\d+)", response)
        if match:
            return int(match.group(1))
        raise ValueError("Could not parse game ticks from response.")

    def get_seed(self):
        """Get world seed from server."""
        response = self.send_command("seed")
        return response.strip().split()[-1][1:-1]

    def get_difficulty(self):
        """Get current difficulty from server."""
        response = self.send_command("difficulty")
        return response.strip().split()[-1]

    def get_version(self):
        """Get server version."""
        response = self.send_command("version")
        return Version.from_string(response)
