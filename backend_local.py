from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import json
from pathlib import Path


app = FastAPI(title="Recettes & Quran API")

# Autoriser toutes les origines pour le test
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Fichiers JSON
RECIPES_FILE = Path(__file__).parent / "client_llm" / "data" / "recipes.json"
SURRAH_FILE = Path(__file__).parent / "client_llm" / "data" / "quran_complete.json"

with open(RECIPES_FILE, "r", encoding="utf-8") as f:
    RECIPES = json.load(f)

with open(SURRAH_FILE, "r", encoding="utf-8") as f:
    SURRAH = json.load(f)

# Routes API
@app.get("/api/recipes")
async def get_recipes():
    return RECIPES

@app.get("/api/surrah")
async def get_surrah():
    return SURRAH

# Simuler un LLM distant
@app.post("/api/recipes_suggestion")
async def suggest_recipe(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    # Simple simulation : filtrer les recettes existantes ou générer un message
    matches = [r for r in RECIPES if prompt.lower() in map(str.lower, r["ingredients"])]
    if matches:
        return {"completion": "\n".join([f"{r['name']} - {', '.join(r['ingredients'])}" for r in matches])}
    return {"completion": f"Recette générée par LLM distant pour '{prompt}' (simulation)"}