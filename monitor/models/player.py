import os
import requests


class Player:
    def __init__(self, username: str, status: str = "offline"):
        self.username = username
        self.status = status
        self.face_path = self.save_player_face()

    def update_status(self, new_status: str):
        self.status = new_status

    def save_player_face(self, size: int = 64, folder: str = "data/face") -> str:
        """
        Fetch a player's face image by username and save it locally.
        Tries Crafatar first, falls back to Minotar if unavailable.
        Returns the local file path.
        """
        os.makedirs(folder, exist_ok=True)

        # Build URLs
        crafatar_url = f"https://crafatar.com/avatars/{self.username}?size={size}&overlay"
        minotar_url = f"https://minotar.net/avatar/{self.username}/{size}.png"

        # Try Crafatar first
        try:
            r = requests.get(crafatar_url, timeout=5)
            if r.status_code == 200:
                img_data = r.content
            else:
                raise Exception("Crafatar failed")
        except Exception:
            # Fallback to Minotar
            r = requests.get(minotar_url, timeout=5)
            img_data = r.content

        # Save to file
        file_path = os.path.join(folder, f"{self.username}.png")
        with open(file_path, "wb") as f:
            f.write(img_data)

        return file_path

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "status": self.status,
            "face_path": self.face_path,
        }
