import json
import os

SAVE_FILE = "savegame.json"

def save_game(player, unlocked_level2):
    data = {
        "coins": player.coins,
        "owned_weapons": list(player.owned_weapons),
        "current_weapon": player.current_weapon,
        "unlocked_level2": unlocked_level2
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_game(player):
    if not os.path.exists(SAVE_FILE):
        return False, False
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    player.coins = data.get("coins", 0)
    player.owned_weapons = set(data.get("owned_weapons", ["Glock"]))
    player.current_weapon = data.get("current_weapon", "Glock")
    unlocked_level2 = data.get("unlocked_level2", False)
    return True, unlocked_level2
