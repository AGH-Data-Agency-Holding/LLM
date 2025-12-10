import requests
from client_llm.recipe_db import search_recipes_local

# URL du backend pour le LLM distant (si disponible)
BACKEND_LLM_URL = "http://127.0.0.1:8000/api/recipes_suggestion"

def generate_local(prompt: str) -> str:
    """
    Appel du LLM local (par ex. Mistral via llama-cli)
    """
    import subprocess

    cmd = [
        "./llama-cli",
        "-m", "/Users/nouamanebahij/models/mistral-7b-v0.1.Q4_K_M.gguf",
        "-p", prompt,
        "--ctx-size", "512",
        "--batch-size", "1",
        "--threads", "4",
        "--temp", "0.7",
        "--top_p", "0.95",
        "--repeat-last-n", "64",
        "--repeat-penalty", "1.1"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def generate_remote(prompt: str) -> str:
    """
    Appel du backend distant
    """
    try:
        response = requests.post(BACKEND_LLM_URL, json={"prompt": prompt}, timeout=5)
        if response.status_code == 200:
            return response.json().get("completion", "")
        else:
            return f"Erreur backend : {response.status_code}"
    except requests.exceptions.RequestException:
        return "Impossible de contacter le serveur distant."

def generate_recipe(prompt: str, use_local=True) -> str:
    """
    Décide si on utilise le LLM local ou distant
    """
    if use_local:
        return generate_local(prompt)
    else:
        return generate_remote(prompt)