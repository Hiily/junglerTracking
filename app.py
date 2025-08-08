from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json

# Charger le fichier déjà extrait
with open("positions.json", "r", encoding="utf-8") as f:
    positions_data = json.load(f)

app = FastAPI()

# Servir le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/positions/{team}/{time_sec}")
def get_positions(team: str, time_sec: int):
    """
    Retourne toutes les positions de `team` dans l'intervalle [time_sec, time_sec + 30)
    """
    if team not in positions_data:
        return {"error": "Team inconnue"}

    points = [
        p for p in positions_data[team]
        if time_sec <= p["time"] < time_sec + 30
    ]
    return points
