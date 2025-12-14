from __future__ import annotations

from monitor.models.version import Version
from . import save_file
from monitor.utils.time_utils import TimeUtils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rcon_monitor import RconMonitor


class Snapshot:
    """Represents a single snapshot of server state."""

    def __init__(self, monitor: RconMonitor, player_count=0, max_players=0, player_names=None,
                 daytime_ticks=0, time_clock="", time_period="", time_dhms=None,
                 seed="", difficulty="", version=None, error="", path=None):
        self.monitor = monitor

        self.player_count = player_count
        self.max_players = max_players
        self.player_names = player_names or []
        self.daytime_ticks = daytime_ticks
        self.gametime_ticks = 0
        self.gametime_ticks_updated = False
        self.time_clock = time_clock
        self.time_period = time_period
        self.time_dhms = time_dhms or TimeUtils.DHMS()
        self.seed = seed
        self.difficulty = difficulty
        self.version = version or Version()
        self.error = error
        self.path = path

    def reset(self):
        """Reset snapshot data."""
        self.player_count = 0
        self.max_players = 0
        self.player_names = []
        self.daytime_ticks = 0
        self.gametime_ticks_updated = False
        self.time_clock = ""
        self.time_period = ""
        self.time_dhms = TimeUtils.DHMS()
        self.seed = ""
        self.difficulty = ""
        self.version = Version()
        self.error = ""

    def update_meta(self):
        """Enrich snapshot with meta info."""
        try:
            daytime_ticks = self.monitor.commander.get_daytime_ticks()
            self.daytime_ticks = daytime_ticks
            gametime_ticks = self.monitor.commander.get_game_ticks()
            self.gametime_ticks_updated = self.check_gametime_ticks_updated(
                gametime_ticks)
            self.gametime_ticks = gametime_ticks
            self.time_clock = TimeUtils.ticks_to_clock(daytime_ticks)
            self.time_period = TimeUtils.ticks_to_period(daytime_ticks)
            self.time_dhms = TimeUtils.gametime_ticks_to_dhms(gametime_ticks)
            self.seed = self.monitor.commander.get_seed()
            self.difficulty = self.monitor.commander.get_difficulty()
            self.version = self.monitor.commander.get_version()
        except Exception as e:
            self.error = str(e)

    def get_player_snapshot(self):
        """Pull /list and update snapshot players."""
        player_data = self.monitor.commander.get_player_data()
        self.player_count = player_data["player_count"]
        self.max_players = player_data["max_players"]
        self.player_names = player_data["player_names"]

    def update_data(self):
        """Update snapshot data from server."""
        self.reset()
        self.update_meta()
        self.get_player_snapshot()

        if not self.error:
            save_file(self.path, self.to_dict())

        return self

    def check_gametime_ticks_updated(self, gametime_ticks) -> bool:
        """Check if gametime ticks were updated in last snapshot."""
        return self.gametime_ticks not in (0, gametime_ticks)

    def to_dict(self):
        """Convert snapshot to a JSON‑friendly dict."""
        return {
            "player_count": self.player_count,
            "max_players": self.max_players,
            "player_names": self.player_names,
            "time_daytime_ticks": self.daytime_ticks,
            "time_gametime_ticks": self.gametime_ticks,
            "server_status": "Running" if self.gametime_ticks_updated else "Idle",
            "time_clock": self.time_clock,
            "time_period": self.time_period,
            "time_dhms": self.time_dhms.to_dict(),
            "seed": self.seed,
            "difficulty": self.difficulty,
            "version": self.version.to_dict(),
            "error": self.error,
        }

    def save(self):
        """Save snapshot to its path as JSON."""
        if self.path:
            save_file(self.path, self.to_dict())
