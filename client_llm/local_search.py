import sqlite3
from pathlib import Path

# Chemins vers les bases de données
SURRAH_DB_PATH = Path(__file__).parent / "surrah.db"
RECIPES_DB_PATH = Path(__file__).parent / "recipes.db"

# --- Recherche Surrah ---
def search_surrah(keyword: str):
    """Recherche une surrah par mot-clé dans les noms arabe, français et anglais."""
    if not SURRAH_DB_PATH.exists():
        print(f"Base de données surrah introuvable : {SURRAH_DB_PATH}")
        return []

    conn = sqlite3.connect(SURRAH_DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT numero, nom_ar, nom_fr, nom_en FROM surrah
        WHERE nom_ar LIKE ? OR nom_fr LIKE ? OR nom_en LIKE ?
    ''', (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = c.fetchall()
    conn.close()
    return results

# --- Recherche Recettes ---
def search_recipes(ingredient: str):
    """Recherche des recettes contenant l'ingrédient dans la base locale."""
    if not RECIPES_DB_PATH.exists():
        print(f"Base de données recettes introuvable : {RECIPES_DB_PATH}")
        return []

    conn = sqlite3.connect(RECIPES_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT name, ingredients, instructions FROM recipes WHERE ingredients LIKE ?",
        (f"%{ingredient}%",)
    )
    results = c.fetchall()
    conn.close()
    return results
def search_recipes_offline(ingredient: str):
    """Mode hors ligne : recherche locale seulement."""
    results = search_recipes(ingredient)
    if results:
        return results
    else:
        print("Aucune recette trouvée localement.")
        return []

# --- Menu principal ---
if __name__ == "__main__":
    print("Choisissez le type de recherche :")
    print("1 - Surrah")
    print("2 - Recette")
    choix = input("Votre choix (1 ou 2) : ")

    if choix == "1":
        keyword = input("Rechercher surrah par mot-clé : ")
        results = search_surrah(keyword)
        if results:
            for r in results:
                print(f"{r[0]} - {r[1]} | {r[2]} | {r[3]}")
        else:
            print("Aucune surrah trouvée.")
    elif choix == "2":
        ingredient = input("Ingrédient à rechercher : ")
        recettes = search_recipes_offline(ingredient)
        for r in recettes:
            print(f"Nom: {r[0]}\nIngrédients: {r[1]}\nInstructions: {r[2]}\n{'-'*40}")
    else:
        print("Choix invalide.")