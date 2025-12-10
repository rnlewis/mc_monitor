import json
import os
import re
import requests
from mcrcon import MCRcon
import threading
from .snapshot import Snapshot
from .status import Status
from . import load_file


class RconMonitor:
    def __init__(self, config_file="config.json"):
        config = load_file(config_file, {})
        self.host = config["host"]
        self.port = config["port"]
        self.password = config["password"]
        self.topic = config["topic"]
        self.snapshot_file = config["snapshot_file"]
        self.status_file = config["status_file"]
        self.data_dir = config["data_dir"]
        self.snapshot = Snapshot(path=os.path.join(
            self.data_dir, self.snapshot_file))
        self.status = Status(path=os.path.join(
            self.data_dir, self.status_file))

        self.stop_event = threading.Event()

    def send_command(self, command: str) -> str:
        with MCRcon(self.host, self.password, port=self.port) as mcr:
            return mcr.command(command)

    def parse_list(self, response: str):
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

    def get_ticks(self):
        """Get current daytime ticks from server."""
        response = self.send_command("time query daytime")
        match = re.search(r"The time is (\d+)", response)
        if match:
            return int(match.group(1))
        raise ValueError("Could not parse daytime ticks from response.")

    def send_ntfy(self, message: str):
        url = f"https://ntfy.sh/{self.topic}"
        requests.post(url, data=message.encode("utf-8")).raise_for_status()

    def load_status(self):
        if os.path.exists(self.status_file):
            with open(self.status_file) as f:
                return json.load(f)
        return {"players": {}, "notify": 0, "message": ""}

    def save_status(self, status):
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)

    def ticks_to_clock(self, ticks: int) -> str:
        hours = ((ticks / 1000) + 6) % 24
        minutes = int((ticks % 1000) * 60 / 1000)
        return f"{int(hours):02d}:{minutes:02d}"

    def ticks_to_period(self, ticks: int) -> str:
        if 0 <= ticks < 1000:
            return "Sunrise"
        elif 1000 <= ticks < 6000:
            return "Morning"
        elif 6000 <= ticks < 12000:
            return "Afternoon"
        elif 12000 <= ticks < 13000:
            return "Sunset"
        elif 13000 <= ticks < 18000:
            return "Evening"
        else:
            return "Night"

    def background_loop(self, interval=15):
        # Run the monitoring loop in the background.
        # Interval is in seconds
        while not self.stop_event.is_set():
            try:
                self.snapshot.update_data(self)
                self.status.update_player_status(self)

            except Exception as e:
                print("Error updating:", e)

            self.stop_event.wait(interval)
