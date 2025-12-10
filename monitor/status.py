from . import load_file, save_file


class Status:
    """Tracks player join/leave events and notification state."""

    def __init__(self, path=None):
        self.players = {}   # {player_name: {"status": "online/joined/left/offline"}}
        self.notify = 0     # flag for whether a notification should be sent
        self.message = ""   # accumulated join/leave messages
        self.path = path

        self.load()

    def update_player_status(self, monitor):
        current_players = monitor.snapshot.players
        tracked = self.players
        notify_flag = 0
        message_log = ""

        # join/leave logic
        for player in current_players:
            if player not in tracked or tracked[player]["status"] in ("offline", "left"):
                tracked[player] = {"status": "joined"}
                notify_flag = 1
                message_log += f"{player} has joined the server!\n"
            elif tracked[player]["status"] == "joined":
                tracked[player]["status"] = "online"

        for player in list(tracked.keys()):
            if player not in current_players:
                if tracked[player]["status"] == "online":
                    tracked[player]["status"] = "left"
                    notify_flag = 1
                    message_log += f"{player} has left the server.\n"
                elif tracked[player]["status"] == "left":
                    tracked[player]["status"] = "offline"
                elif tracked[player]["status"] == "joined":
                    tracked[player]["status"] = "left"
                    notify_flag = 1
                    message_log += f"{player} has left the server.\n"

        self.players = tracked
        self.notify = notify_flag
        self.message = message_log.strip()

        if notify_flag and message_log:
            monitor.send_ntfy(self.message)

        self.save()

        return self

    def to_dict(self):
        return {
            "players": self.players,
            "notify": self.notify,
            "message": self.message,
        }

    def reset(self):
        self.notify = 0
        self.message = ""

    def load(self):
        if self.path:
            loaded = load_file(self.path, {"players": {}})
            self.players = loaded.get("players", {})
            self.notify = loaded.get("notify", 0)
            self.message = loaded.get("message", "")

    def save(self):
        """Save snapshot to its path as JSON."""
        if self.path:
            save_file(self.path, self.to_dict())
