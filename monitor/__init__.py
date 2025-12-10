import json


def load_file(path, fallback):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return fallback


def save_file(path, data, indent=2):
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)
