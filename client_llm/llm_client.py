import requests
import subprocess
from .local_db import search_recipes_local

# -----------------------------
# 🌍 URLs des endpoints
# -----------------------------
BACKEND_RECIPES_URL = "http://127.0.0.1:8000/api/recipes_suggestion"
BACKEND_SURRAH_URL = "http://127.0.0.1:8000/api/surrah_suggestion"
SERVER_LLM_URL = "http://127.0.0.1:8000/ask"  # Serveur LLM centralisé (RAG + Redis)


# -----------------------------
# 🧠 1️⃣ LLM LOCAL (Mistral)
# -----------------------------
def generate_local(prompt: str) -> str:
    """Appel du modèle LLM local (Mistral 7B via llama-cli)."""
    try:
        cmd = [
            "./llama-cli",
            "-m", "/Users/nouamanebahij/AndroidStudioProjects/LLM_CLIENT/models/mistral-7b-v0.1.Q4_K_M.gguf",
            "-p", prompt,
            "--ctx-size", "512",
            "--batch-size", "1",
            "--threads", "4",
            "--temp", "0.7",
            "--top_p", "0.95",
            "--repeat-last-n", "64",
            "--repeat-penalty", "1.1"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Erreur LLM local : {e}"


# -----------------------------
# 🍽️ 2️⃣ MODE OFFLINE (recettes)
# -----------------------------
def generate_recipe_offline(prompt: str) -> str:
    """Recherche locale + génération locale si non trouvé."""
    local_recipes = search_recipes_local(prompt)
    if local_recipes:
        return "Résultats locaux :\n" + "\n".join([r["name"] for r in local_recipes])
    return generate_local(prompt)


# -----------------------------
# 🌐 3️⃣ LLM DISTANT (recettes / sourates)
# -----------------------------
def generate_remote(prompt: str, mode: str = "recipes") -> str:
    """Appel du backend FastAPI (simulé) selon le type."""
    try:
        url = BACKEND_RECIPES_URL if mode == "recipes" else BACKEND_SURRAH_URL
        response = requests.post(url, json={"prompt": prompt}, timeout=5)
        if response.status_code == 200:
            return response.json().get("completion", "")
        return f"Erreur backend {mode} : {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Impossible de contacter le backend {mode} : {e}"


# -----------------------------
# ☁️ 4️⃣ SERVEUR GLOBAL (RAG + Cache Redis)
# -----------------------------
def generate_from_server(prompt: str, app_id: int = 1) -> str:
    """Appel du serveur central LLM (multi-apps avec cache intelligent)."""
    try:
        response = requests.post(
            SERVER_LLM_URL,
            json={"app_id": app_id, "question": prompt},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return f"[{data['source']}] {data['response']}"
        return f"Erreur serveur global : {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Impossible de contacter le serveur global : {e}"


# -----------------------------
# ⚙️ 5️⃣ GESTION DES MODES ET DOMAINE
# -----------------------------
def generate_llm(prompt: str, domain: str = "recipes", mode: str = "local") -> str:
    """
    Gère la génération selon le domaine (recettes/sourates) et le mode (local/remote/server).
    """
    if mode == "local":
        if domain == "recipes":
            return generate_recipe_offline(prompt)
        else:
            return generate_local(f"Sourate liée à : {prompt}")
    elif mode == "remote":
        return generate_remote(prompt, mode=domain)
    elif mode == "server":
        app_id = 1 if domain == "recipes" else 2  # Exemple : 1 = recettes, 2 = Quran
        return generate_from_server(prompt, app_id)
    else:
        return "❌ Mode inconnu. Choisir entre 'local', 'remote', ou 'server'."


# -----------------------------
# 🚀 6️⃣ TEST INTERACTIF
# -----------------------------
if __name__ == "__main__":
    print("=== Client LLM Multi-Domaine ===")
    domain = input("Domaine (recipes / surrah) : ").strip().lower()
    prompt = input("Entrer le prompt ou ingrédient : ").strip()
    mode = input("Mode (local / remote / server) : ").strip().lower()

    print("\n--- Résultat ---")
    print(generate_llm(prompt, domain, mode))