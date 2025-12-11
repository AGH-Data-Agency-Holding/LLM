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

## 🗂️ Structure du Projet
client_llm/
├── init.py
├── backend.py              # Backend FastAPI simulant un serveur distant
├── llm_client.py           # Gestion du LLM local / distant / serveur global
├── main_flow.py            # Flux principal (choix offline / online / server)
├── local_db.py             # Initialisation et recherche dans les DB locales
├── recipe_db           
├── surrah_db        
├── data/
│   ├── recipes.json
│   ├── quran_complete.json
│   
└── README.md

---

## ⚙️ Installation

### 🧩 Prérequis

- Python ≥ 3.9
- FastAPI + Uvicorn
- Modèle Mistral téléchargé pour `llama-cli`
- (Optionnel) Redis si tu veux tester le cache serveur global

### 🧰 Installation des dépendances
```bash
pip install fastapi uvicorn requests pydantic
python3 -m client_llm.main_flow
Ingrédient à rechercher : tomate
Mode (offline/online/server) : offline
Résultats locaux :
- Quiche tomates et épinards

Mode Online (Backend Local FastAPI)
uvicorn client_llm.backend:app --reload
python3 -m client_llm.main_flow
Mode (offline/online/server) : online
Aucune recette sur le serveur. Génération LLM distant...
Recette générée par LLM distant pour 'Recette avec l'ingrédient tomate' (simulation)
Mode Server (RAG + Redis)
python3 -m client_llm.main_flow
Mode (offline/online/server) : server
[Cache Redis] La première sourate du Coran est Al-Fatiha.
