from . import save_file


class Snapshot:
    """Represents a single snapshot of server state."""

    def __init__(self, player_count=0, max_players=0, players=None,
                 daytime_ticks=0, time_clock="", time_period="",
                 seed="", difficulty="", version="", error="", path=None):
        self.player_count = player_count
        self.max_players = max_players
        self.players = players or []
        self.daytime_ticks = daytime_ticks
        self.time_clock = time_clock
        self.time_period = time_period
        self.seed = seed
        self.difficulty = difficulty
        self.version = version
        self.error = error
        self.path = path

    def reset(self):
        """Reset snapshot data."""
        self.player_count = 0
        self.max_players = 0
        self.players = []
        self.daytime_ticks = 0
        self.time_clock = ""
        self.time_period = ""
        self.seed = ""
        self.difficulty = ""
        self.version = ""
        self.error = ""

    def update_meta(self, monitor):
        """Enrich snapshot with meta info."""
        try:
            daytime_ticks = monitor.get_ticks()
            self.daytime_ticks = daytime_ticks
            self.time_clock = monitor.ticks_to_clock(daytime_ticks)
            self.time_period = monitor.ticks_to_period(daytime_ticks)
            self.seed = monitor.send_command("seed").strip()
            self.difficulty = monitor.send_command("difficulty").strip()
            self.version = monitor.send_command(
                "version").strip().splitlines()[0]
        except Exception as e:
            self.error = str(e)

    def get_player_snapshot(self, monitor):
        """Pull /list and update snapshot players."""
        list_resp = monitor.send_command("list")
        parsed = monitor.parse_list(list_resp)
        self.player_count = parsed["player_count"]
        self.max_players = parsed["max_players"]
        self.players = parsed["players"]

    def update_data(self, monitor):
        """Update snapshot data from server."""
        self.reset()
        self.update_meta(monitor)
        self.get_player_snapshot(monitor)

        if not self.error:
            save_file(self.path, self.to_dict())

        return self

    def to_dict(self):
        """Convert snapshot to a JSON‑friendly dict."""
        return {
            "player_count": self.player_count,
            "max_players": self.max_players,
            "players": self.players,
            "time_daytime_ticks": self.daytime_ticks,
            "time_clock": self.time_clock,
            "time_period": self.time_period,
            "seed": self.seed,
            "difficulty": self.difficulty,
            "version": self.version,
            "error": self.error,
        }

    def save(self):
        """Save snapshot to its path as JSON."""
        if self.path:
            save_file(self.path, self.to_dict())
