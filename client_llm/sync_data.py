import requests
import sqlite3
from pathlib import Path

# ==============================
# 📁 Chemins vers les bases locales
# ==============================
RECIPES_DB = Path(__file__).parent / "recipes.db"
SURRAH_DB = Path(__file__).parent / "surrah.db"

# ==============================
# 🌐 URLs du backend FastAPI
# ==============================
RECIPES_URL = "http://127.0.0.1:8000/api/recipes"
SURRAH_URL = "http://127.0.0.1:8000/api/surrah"


# ==============================
# 🍽️ SYNCHRONISATION DES RECETTES
# ==============================
def sync_recipes():
    """Synchroniser les recettes locales avec le backend."""
    if not RECIPES_DB.exists():
        print(f"⚠️ Base de données locale introuvable : {RECIPES_DB}")
        return

    try:
        response = requests.get(RECIPES_URL, timeout=5)
        response.raise_for_status()
        recipes = response.json()

        conn = sqlite3.connect(RECIPES_DB)
        c = conn.cursor()

        for r in recipes:
            c.execute("""
                INSERT OR REPLACE INTO recipes (id, name, ingredients, instructions, type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                r["id"], r["name"], ",".join(r["ingredients"]),
                r["instructions"], r.get("type", "")
            ))

        conn.commit()
        conn.close()
        print("✅ Synchronisation des recettes réussie.")
    except Exception as e:
        print("❌ Erreur lors de la synchronisation des recettes :", e)


# ==============================
# 📖 SYNCHRONISATION DES SOURATES
# ==============================
def sync_surrah():
    """Synchroniser les sourates locales avec le backend."""
    if not SURRAH_DB.exists():
        print(f"⚠️ Base de données locale introuvable : {SURRAH_DB}")
        return

    try:
        response = requests.get(SURRAH_URL, timeout=5)
        response.raise_for_status()
        surrahs = response.json()

        conn = sqlite3.connect(SURRAH_DB)
        c = conn.cursor()

        for s in surrahs:
            # --- Insertion des informations de la sourate ---
            c.execute("""
            INSERT OR REPLACE INTO surrah
            (numero, nom_ar, nom_fr, nom_en, ordre_mushaf, type_fr, type_ar, type_en, nombre_versets, audio_lien)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["numero"], s["nom_ar"], s["nom_fr"], s["nom_en"],
                s["ordre_mushaf"], s["type"]["fr"], s["type"]["ar"], s["type"]["en"],
                s["nombre_versets"], s["audio_lien"]
            ))

            # --- Insertion des versets ---
            for v in s["versets"]:
                c.execute("""
                INSERT OR REPLACE INTO versets (surrah_numero, numero, ar, fr, en)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    s["numero"], v["numero"], v["ar"], v["fr"], v["en"]
                ))

        conn.commit()
        conn.close()
        print("✅ Synchronisation du Coran réussie.")
    except Exception as e:
        print("❌ Erreur lors de la synchronisation des sourates :", e)


# ==============================
# 🧩 MODE HORS-LIGNE
# ==============================
def sync_offline():
    print("⚙️ Mode hors-ligne activé : aucune synchronisation effectuée.")


# ==============================
# 🚀 TEST RAPIDE
# ==============================
if __name__ == "__main__":
    print("=== 🌐 Synchronisation des bases locales ===")
    mode = input("Mode (online/offline) : ").strip().lower()

    if mode == "online":
        sync_recipes()
        sync_surrah()
    else:
        sync_offline()

    print("\n=== 🔎 Vérification des données locales ===")

    # --- Vérifier les recettes ---
    if RECIPES_DB.exists():
        conn = sqlite3.connect(RECIPES_DB)
        c = conn.cursor()
        c.execute("SELECT name, ingredients FROM recipes LIMIT 3")
        for row in c.fetchall():
            print(f"🍽️ {row[0]} | Ingrédients : {row[1]}")
        conn.close()

    # --- Vérifier les sourates ---
    if SURRAH_DB.exists():
        conn = sqlite3.connect(SURRAH_DB)
        c = conn.cursor()
        c.execute("SELECT numero, nom_fr FROM surrah LIMIT 3")
        for row in c.fetchall():
            print(f"📖 Sourate {row[0]} - {row[1]}")
        conn.close()

    print("\n✅ Synchronisation terminée.")