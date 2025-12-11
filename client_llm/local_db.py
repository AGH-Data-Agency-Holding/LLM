import sqlite3
import json
from pathlib import Path

# ==============================
# 🔹 Fichiers & chemins de données
# ==============================
BASE_PATH = Path(__file__).parent / "data"

DB_RECIPES = Path(__file__).parent / "recipes.db"
DB_SURRAH = Path(__file__).parent / "surrah.db"

JSON_RECIPES = BASE_PATH / "recipes.json"
JSON_SURRAH = BASE_PATH / "quran_complete.json"

# ==============================
# 🍽️ Partie 1 — RECETTES
# ==============================
def init_recipes_db():
    """Créer la base SQLite pour les recettes et y charger les données JSON."""
    if not JSON_RECIPES.exists():
        print(f"⚠️ Fichier introuvable : {JSON_RECIPES}")
        return

    with open(JSON_RECIPES, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    conn = sqlite3.connect(DB_RECIPES)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        ingredients TEXT,
        instructions TEXT,
        type TEXT
    )
    """)

    for r in recipes:
        c.execute("""
        INSERT OR REPLACE INTO recipes (id, name, ingredients, instructions, type)
        VALUES (?, ?, ?, ?, ?)
        """, (
            r.get("id"),
            r.get("name", "Nom inconnu"),
            ",".join(r.get("ingredients", [])),
            r.get("instructions", ""),
            r.get("type", "")
        ))

    conn.commit()
    conn.close()
    print("✅ Base de données RECETTES initialisée.")


def search_recipes_local(keyword: str):
    """Recherche des recettes dans la base locale par mot-clé."""
    conn = sqlite3.connect(DB_RECIPES)
    c = conn.cursor()
    like_pattern = f"%{keyword.lower()}%"
    c.execute("""
        SELECT id, name, ingredients, instructions, type
        FROM recipes
        WHERE LOWER(ingredients) LIKE ? OR LOWER(name) LIKE ?
    """, (like_pattern, like_pattern))
    rows = c.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "ingredients": r[2].split(",") if r[2] else [],
            "instructions": r[3],
            "type": r[4]
        } for r in rows
    ]

# ==============================
# 📖 Partie 2 — QURAN (Surrah + Versets)
# ==============================
def init_surrah_db():
    """Créer la base SQLite pour les sourates et y charger le contenu JSON."""
    if not JSON_SURRAH.exists():
        print(f"⚠️ Fichier introuvable : {JSON_SURRAH}")
        return

    with open(JSON_SURRAH, "r", encoding="utf-8") as f:
        surrahs = json.load(f)

    conn = sqlite3.connect(DB_SURRAH)
    c = conn.cursor()

    # Table des sourates
    c.execute("""
    CREATE TABLE IF NOT EXISTS surrah (
        numero INTEGER PRIMARY KEY,
        nom_ar TEXT,
        nom_fr TEXT,
        nom_en TEXT,
        ordre_mushaf INTEGER,
        type_fr TEXT,
        type_ar TEXT,
        type_en TEXT,
        nombre_versets INTEGER,
        audio_lien TEXT
    )
    """)

    # Table des versets
    c.execute("""
    CREATE TABLE IF NOT EXISTS versets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surrah_numero INTEGER,
        numero INTEGER,
        ar TEXT,
        fr TEXT,
        en TEXT,
        FOREIGN KEY(surrah_numero) REFERENCES surrah(numero)
    )
    """)

    for surrah in surrahs:
        c.execute("""
        INSERT OR REPLACE INTO surrah
        (numero, nom_ar, nom_fr, nom_en, ordre_mushaf, type_fr, type_ar, type_en, nombre_versets, audio_lien)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            surrah["numero"],
            surrah["nom_ar"], surrah["nom_fr"], surrah["nom_en"],
            surrah["ordre_mushaf"],
            surrah["type"]["fr"], surrah["type"]["ar"], surrah["type"]["en"],
            surrah["nombre_versets"],
            surrah["audio_lien"]
        ))

        for v in surrah["versets"]:
            c.execute("""
            INSERT OR REPLACE INTO versets (surrah_numero, numero, ar, fr, en)
            VALUES (?, ?, ?, ?, ?)
            """, (
                surrah["numero"],
                v["numero"],
                v["ar"], v["fr"], v["en"]
            ))

    conn.commit()
    conn.close()
    print("✅ Base de données QURAN initialisée.")


def search_surrah_local(keyword: str):
    """Recherche d'une sourate dans la base locale."""
    conn = sqlite3.connect(DB_SURRAH)
    c = conn.cursor()
    like_pattern = f"%{keyword}%"
    c.execute("""
        SELECT numero, nom_ar, nom_fr, nom_en, audio_lien
        FROM surrah
        WHERE nom_ar LIKE ? OR nom_fr LIKE ? OR nom_en LIKE ?
    """, (like_pattern, like_pattern, like_pattern))
    results = c.fetchall()
    conn.close()

    return [
        {
            "numero": r[0],
            "nom_ar": r[1],
            "nom_fr": r[2],
            "nom_en": r[3],
            "audio_lien": r[4]
        }
        for r in results
    ]

# ==============================
# 🧩 TEST DIRECT
# ==============================
if __name__ == "__main__":
    print("=== Initialisation des bases locales ===")
    init_recipes_db()
    init_surrah_db()

    # Test de recherche
    kw = input("Mot-clé : ")
    print("\n🔹 Recettes trouvées :")
    for r in search_recipes_local(kw):
        print(f"- {r['name']} ({', '.join(r['ingredients'])})")

    print("\n🔹 Sourates trouvées :")
    for s in search_surrah_local(kw):
        print(f"- {s['numero']} {s['nom_fr']} ({s['nom_ar']}) | Audio: {s['audio_lien']}")