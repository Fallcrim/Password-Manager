import os
import json


def load_config():
    if os.path.isfile("config.json"):
        with open("config.json") as f:
            return json.load(f)
    else:
        return dict()


def save_config(config: dict):
    with open("config.json", "w") as f:
        json.dump(config, f)
