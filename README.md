# 🤖 Client LLM — Recettes & Quran

## 📘 Aperçu

Ce module `client_llm` implémente un **client intelligent** capable de communiquer :
- avec un **LLM local** (via `llama-cli` et le modèle *Mistral 7B*),
- avec un **backend distant FastAPI** (simulation locale),
- ou avec un **serveur LLM global** basé sur RAG + Redis (centralisé).

L’objectif est de fournir un système **hybride** et **résilient**, capable de fonctionner :
- 🔹 en **mode hors ligne (offline)** — via SQLite et le LLM local,
- 🔹 en **mode en ligne (online)** — via un backend FastAPI local,
- 🔹 en **mode serveur (server)** — via une API centralisée (RAG + cache Redis).

---

## 🧱 Fonctionnalités principales

### 🍳 Gestion des Recettes
- Base locale `recipes.db` initialisée à partir de `data/recipes.json`
- Recherche rapide par ingrédient
- Génération de suggestions via le LLM local ou distant

### 📖 Gestion du Coran
- Base locale `surrah.db` créée depuis `data/quran_complete.json`
- Recherche par nom de sourate (arabe, français, anglais)
- Lecture de liens audio associés aux sourates

### 🧠 Modes de fonctionnement
| Mode | Source | Description |
|------|---------|-------------|
| **offline** | Local DB + LLM local | Fonctionne sans Internet |
| **online** | Backend FastAPI local | Requêtes simulées au serveur local |
| **server** | Serveur LLM RAG | Connexion à l’API centralisée avec cache Redis |

---
## ✔️ Avantages du Projet

Ce projet offre une architecture flexible, performante et adaptée à différents environnements d’exécution.

### 🔹 1. Multi-mode de fonctionnement
- **Offline** : fonctionne entièrement sans connexion réseau grâce aux bases locales SQLite et au modèle LLM quantifié (Mistral).
- **Online** : interagit avec le backend FastAPI pour récupérer ou synchroniser les données.
- **Server** : se connecte au serveur LLM global (RAG + Redis) pour bénéficier du cache et de la génération contextuelle.

### 🔹 2. Architecture modulaire et extensible
- Séparation claire entre les couches :
    - `local_db.py` : gestion des bases locales (Recettes + Coran)
    - `llm_client.py` : communication avec les modèles IA (local/distant)
    - `backend_local.py` : API FastAPI simulée pour test local
- Facile à étendre avec d’autres domaines (ex. Qissas, Hadith, etc.).

### 🔹 3. Intégration hybride (LLM + données structurées)
- Combine la **génération par IA** (LLM Mistral) avec la **recherche locale rapide** (SQLite).
- Permet des suggestions intelligentes tout en gardant la cohérence des données.

### 🔹 4. Performances et robustesse
- Cache intelligent pour réduire le coût des appels au LLM.
- Chargement rapide des données locales (moins de 200 ms).
- Inférence locale optimisée (modèle quantifié ~300 Mo).

### 🔹 5. Facilité de test et de déploiement
- Compatible **terminal / mobile / backend**.
- Testable via `python3 -m client_llm.main_flow` sans dépendances externes lourdes.
- Intégration directe dans Android Studio pour développement mobile.

---

🚀 **En résumé :**
> `client_llm` agit comme un cerveau local intelligent, capable d’utiliser un modèle IA en mode hors-ligne, de communiquer avec un serveur distant, et de s’intégrer dans un système RAG complet.
---

## 🗂️ Structure du Projet


```text
client_llm/
├── __init__.py
├── backend.py              # Backend FastAPI simulant un serveur distant
├── llm_client.py           # Gestion du LLM local / distant / serveur global
├── main_flow.py            # Flux principal (choix offline / online / server)
├── local_db.py             # Initialisation et recherche dans les DB locales (Recettes & Quran)
├── recipe_db               # Base locale SQLite des recettes
├── surrah_db               # Base locale SQLite des sourates
├── data/
│   ├── recipes.json        # Données JSON des recettes
│   ├── quran_complete.json # Données JSON complètes du Coran
│   
└── README.md

``` 
## ⚙️ Installation

### 🧩 Prérequis

- Python ≥ 3.9
- FastAPI + Uvicorn
- Modèle Mistral téléchargé pour `llama-cli`
- (Optionnel) Redis si tu veux tester le cache serveur global

### 🧰 Installation des dépendances
```bash
pip install fastapi uvicorn requests pydantic

🔸 Mode Offline
python3 -m client_llm.main_flow
Ingrédient à rechercher : tomate
Mode (offline/online/server) : offline
Résultats locaux :
- Quiche tomates et épinards

🔸 Mode Online (Backend Local FastAPI)
python3 -m client_llm.main_flow
Mode (offline/online/server) : online
Aucune recette sur le serveur. Génération LLM distant...
Recette générée par LLM distant pour 'Recette avec l'ingrédient tomate' (simulation)

🔸 Mode Server (RAG + Redis)
python3 -m client_llm.main_flow
Mode (offline/online/server) : server
[Cache Redis] La première sourate du Coran est Al-Fatiha.
