import json
import os
import re
import requests
from mcrcon import MCRcon
import threading

from monitor.commands import Commander
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

        self.snapshot = Snapshot(self, path=os.path.join(
            self.data_dir, self.snapshot_file))
        self.status = Status(self, path=os.path.join(
            self.data_dir, self.status_file))

        self.commander = Commander(self)

        self.stop_event = threading.Event()

    def send_command(self, command: str) -> str:
        with MCRcon(self.host, self.password, port=self.port) as mcr:
            return mcr.command(command)

    def send_ntfy(self, message: str):
        url = f"https://ntfy.sh/{self.topic}"
        requests.post(url, data=message.encode("utf-8")).raise_for_status()

    def background_loop(self, interval=15):
        # Run the monitoring loop in the background.
        # Interval is in seconds
        while not self.stop_event.is_set():
            try:
                self.snapshot.update_data()
                self.status.update_player_status()

            except Exception as e:
                print("Error updating:", e)

            self.stop_event.wait(interval)
