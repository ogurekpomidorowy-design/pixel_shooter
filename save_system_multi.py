import json
import os
SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_game_named(player, unlocked_level2, save_name):
    data = {
        "coins": player.coins,
        "owned_weapons": list(player.owned_weapons),
        "current_weapon": player.current_weapon,
        "unlocked_level2": unlocked_level2
    }
    path = os.path.join(SAVE_DIR, f"save_{save_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def list_saves():
    return [f[5:-5] for f in os.listdir(SAVE_DIR) if f.startswith("save_") and f.endswith(".json")]

def load_game_named(player, save_name):
    path = os.path.join(SAVE_DIR, f"save_{save_name}.json")
    if not os.path.exists(path):
        return False, False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    player.coins = data.get("coins", 0)
    player.owned_weapons = set(data.get("owned_weapons", ["Glock"]))
    player.current_weapon = data.get("current_weapon", "Glock")
    unlocked_level2 = data.get("unlocked_level2", False)
    return True, unlocked_level2
