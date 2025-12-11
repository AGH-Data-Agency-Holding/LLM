import requests
import sqlite3
from .local_db import search_recipes_local, search_surrah_local
from .llm_client import generate_remote, generate_from_server, generate_recipe_offline
# --- URLs du backend ---
RECIPES_BACKEND_URL = "http://127.0.0.1:8000/api/recipes"
SURRAH_BACKEND_URL = "http://127.0.0.1:8000/api/surrah"


# ==============================
# 🍽️ RECETTES : Backend + Local
# ==============================
def get_backend_recipes(ingredient: str):
    """Récupère les recettes depuis le backend (FastAPI local)."""
    try:
        response = requests.get(RECIPES_BACKEND_URL, timeout=5)
        response.raise_for_status()
        recipes = response.json()
        filtered = [
            r for r in recipes if ingredient.lower() in map(str.lower, r["ingredients"])
        ]
        return filtered
    except Exception as e:
        print("Erreur backend recettes :", e)
        return []


# ==============================
# 📖 SOURATES : Backend + Local
# ==============================
def get_backend_surrah(keyword: str):
    """Récupère les sourates depuis le backend (FastAPI local)."""
    try:
        response = requests.get(SURRAH_BACKEND_URL, timeout=5)
        response.raise_for_status()
        surrahs = response.json()
        filtered = [
            s for s in surrahs
            if keyword.lower() in s["nom_fr"].lower()
            or keyword.lower() in s["nom_en"].lower()
            or keyword in s["nom_ar"]
        ]
        return filtered
    except Exception as e:
        print("Erreur backend Quran :", e)
        return []


# ==============================
# 🚀 FLUX PRINCIPAL
# ==============================
def main():
    print("=== 🌐 Client LLM Multi-Domaine ===")
    domain = input("Choisir le domaine (recipes / surrah) : ").strip().lower()
    keyword = input("Mot-clé à rechercher : ").strip()
    mode = input("Mode (offline / online / server) : ").strip().lower()

    # --- Domaine RECETTES ---
    if domain == "recipes":
        if mode == "offline":
            results = generate_recipe_offline(keyword)
            print(f"\nRésultats hors-ligne pour '{keyword}':\n{results}")
        elif mode == "online":
            backend_results = get_backend_recipes(keyword)
            if backend_results:
                print(f"\n{len(backend_results)} recette(s) trouvée(s) :\n")
                for r in backend_results:
                    print(f"Nom: {r['name']}\nIngrédients: {', '.join(r['ingredients'])}\nInstructions: {r['instructions']}\n{'-'*40}")
            else:
                print("Aucune recette sur le serveur. Génération LLM distant...")
                print(generate_remote(f"Recette avec {keyword}"))
        elif mode == "server":
            print("Appel du serveur LLM (RAG + Redis)...")
            result = generate_from_server(f"Recette avec {keyword}", app_id=1)
            print(result)
        else:
            print("❌ Mode inconnu. Choisir offline, online ou server.")

    # --- Domaine QURAN / SURRAH ---
    elif domain == "surrah":
        if mode == "offline":
            local_results = search_surrah_local(keyword)
            print(f"\n{len(local_results)} sourate(s) trouvée(s) localement :")
            for s in local_results:
                print(f"{s['numero']} - {s['nom_fr']} ({s['nom_ar']}) | Audio: {s['audio_lien']}")
        elif mode == "online":
            backend_results = get_backend_surrah(keyword)
            print(f"\n{len(backend_results)} sourate(s) trouvée(s) sur le serveur :")
            for s in backend_results:
                print(f"{s['numero']} - {s['nom_fr']} ({s['nom_ar']}) | Audio: {s['audio_lien']}")
        elif mode == "server":
            print("Appel du serveur LLM (Quran / RAG)...")
            result = generate_from_server(f"Verset ou explication de {keyword}", app_id=2)
            print(result)
        else:
            print("❌ Mode inconnu. Choisir offline, online ou server.")

    else:
        print("❌ Domaine inconnu. Choisir entre 'recipes' ou 'surrah'.")


# ==============================
# 🧩 TEST
# ==============================
if __name__ == "__main__":
    main()