import json
import random

WISHES_FILE = "data/wishes.json"


def get_random_wish():
    with open(WISHES_FILE, "r", encoding="utf-8") as f:
        wishes = json.load(f)

    return random.choice(wishes)