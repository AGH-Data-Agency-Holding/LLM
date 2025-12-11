import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "recipes.db"

def search_recipes(ingredient: str):
    """Recherche des recettes contenant l'ingrédient dans la base locale."""
    if not DB_PATH.exists():
        print(f"Base de données introuvable : {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT name, ingredients, instructions FROM recipes WHERE ingredients LIKE ?",
        (f"%{ingredient}%",)
    )
    results = c.fetchall()
    conn.close()
    return results

def search_recipes_offline(ingredient: str):
    """
    Mode hors ligne : recherche locale seulement.
    """
    results = search_recipes(ingredient)
    if results:
        return results
    else:
        print("Aucune recette trouvée localement.")
        return []

# Test rapide
if __name__ == "__main__":
    ingredient = input("Ingrédient à rechercher : ")
    recettes = search_recipes_offline(ingredient)
    for r in recettes:
        print(f"Nom: {r[0]}\nIngrédients: {r[1]}\nInstructions: {r[2]}\n{'-'*40}")