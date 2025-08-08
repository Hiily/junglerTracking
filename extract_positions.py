import json
import os

INTERVAL_SEC = 15  # secondes

teams_data = {
    "CLA": {
        "jungler": "CLA SPOOKY",
        "files": [
            "games/cla_game1.jsonl",
            "games/cla_game2.jsonl",
            "games/cla_game3.jsonl",
            "games/cla_game4.jsonl",
            "games/cla_game5.jsonl",
        ]
    },
    "PCS": {
        "jungler": "PCS Frost",
        "files": [
            "games/pcs_game1.jsonl",
            "games/pcs_game2.jsonl",
            "games/pcs_game3.jsonl",
            "games/pcs_game4.jsonl",
            "games/pcs_game5.jsonl",
        ]
    }
}

positions_data = {team: [] for team in teams_data.keys()}

for team, data in teams_data.items():
    jungler_name = data["jungler"].lower()

    for file in data["files"]:
        if not os.path.exists(file):
            print(f"[!] Fichier manquant : {file}")
            continue

        start_time = None
        next_capture_time = 0
        jungler_side = None  # blue ou red

        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Étape 1 : si on est dans la phase champ select, détecter le side du jungler
                if "teamOne" in event and "teamTwo" in event and jungler_side is None:
                    # teamOne = blue, teamTwo = red
                    if any(p.get("summonerName", "").lower() == jungler_name for p in event["teamOne"]):
                        jungler_side = "blue"
                    elif any(p.get("summonerName", "").lower() == jungler_name for p in event["teamTwo"]):
                        jungler_side = "red"

                # Étape 2 : on ne commence à enregistrer que si c’est un event avec participants
                if "participants" not in event:
                    continue

                gt_sec = event.get("gameTime", 0) / 1000.0
                if start_time is None:
                    start_time = gt_sec

                game_time_sec = gt_sec - start_time
                if game_time_sec < 0:
                    continue
                if game_time_sec > 1800:
                    break

                for p in event["participants"]:
                    if p.get("playerName", "").lower() == jungler_name:
                        if game_time_sec >= next_capture_time:
                            positions_data[team].append({
                                "time": round(game_time_sec, 2),
                                "minute": round(game_time_sec / 60, 2),
                                "x": p["position"]["x"],
                                "y": p["position"]["z"],
                                "value": 1,
                                "side": jungler_side or "unknown"
                            })
                            next_capture_time += INTERVAL_SEC
                            break 

with open("positions.json", "w", encoding="utf-8") as out:
    json.dump(positions_data, out, indent=2)

print("[✔] Extraction terminée → positions.json créé avec side détecté en champ select")
