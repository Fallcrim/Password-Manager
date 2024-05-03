import os
import json


def load_config():
    if os.path.isfile("settings.json"):
        with open("settings.json") as f:
            return json.load(f)
    else:
        return dict()


def _save_config(config: dict):
    with open("settings.json") as f:
        json.dump(config, f)
