# client_llm/main_flow.py
from recipe_search import search_recipes
import requests

BACKEND_URL = "http://127.0.0.1:8000/api/recipes"  # ton serveur FastAPI local

def get_backend_recipes(ingredient: str):
    """Récupère les recettes depuis le serveur distant contenant l'ingrédient."""
    try:
        response = requests.get(BACKEND_URL)
        response.raise_for_status()
        recipes = response.json()
        # Filtrer par ingrédient
        filtered = [r for r in recipes if ingredient in r["ingredients"]]
        return filtered
    except Exception as e:
        print("Erreur serveur distant :", e)
        return []

def main():
    ingredient = input("Ingrédient à rechercher : ")

    # 1️⃣ Recherche locale
    local_results = search_recipes(ingredient)
    if local_results:
        print("\nRésultats locaux :")
        for r in local_results:
            print(f"Nom: {r[0]}\nIngrédients: {r[1]}\nInstructions: {r[2]}\n{'-'*40}")
    else:
        print("Aucune recette trouvée localement.")
        # 2️⃣ Génération via LLM local
        print("\nGénération de recette avec LLM local...")
        llm_result = generate_recipe_offline(f"Recette avec l'ingrédient {ingredient}")
        print(llm_result)

    # 🔒 Mode hors ligne : on n'appelle jamais le serveur distant
    print("\nMode hors ligne activé : aucune requête serveur effectuée.")

if __name__ == "__main__":
    main()