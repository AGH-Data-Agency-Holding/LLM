# 🚀 LLM RAG & Caching API

## 📘 Overview
Ce projet implémente une **API RESTful** basée sur **FastAPI** permettant de poser des questions à un **LLM** en s'appuyant sur une architecture **RAG (Retrieval-Augmented Generation)** et un **cache Redis** pour réduire la latence. Plusieurs applications (Recettes, Coran, Qissas, etc.) coexistent de manière isolée grâce à un système de **multi-contextes** indexé par `app_id`.

L'objectif est de fournir un service rapide, scalable et extensible, tout en assurant une séparation claire entre les données, la logique métier et l'API.

---

## 🧠 Fonctionnalités Principales

### 🔍 RAG (Retrieval-Augmented Generation)
* Utilisation d'embeddings (`multi-qa-mpnet-base-dot-v1`) pour retrouver les documents les plus pertinents.
* Génération de réponses contextualisées grâce au modèle LLM (`mistral:7b`).
* Données RAG stockées dans `/data` (embeddings `.pt` et fichiers textuels `.json`).

### ⚡ Cache Intelligent (Redis)
* Les réponses précédemment générées sont mises en cache.
* Le système répond instantanément si une réponse est présente dans Redis.
* Réduction majeure du coût et du temps d'inférence.

### 🧱 Multi-Application
* Plusieurs jeux de données indépendants : Recette, Quran, Qissas, etc.
* Chaque application possède ses propres embeddings et documents.
* Le `app_id` contrôle la sélection du contexte.

---

## 🗂️ Structure du Projet
```
.
├── 0-data-processing/
├── 1-cache/
├── 2-isolation/
│   ├── api.py
│   ├── config.py
│   ├── prompts.py
│   ├── server_utils_optimised.py
│   ├── documentation/
├── data/
│   ├── quran_embeddings.pt
│   ├── quran_handling.json
│   ├── recette_embeddings.pt
│   ├── recette_handling.json
│   ├── qissas_embeddings.pt
│   ├── qissas_handling.json
├── data_handling/
└── README.md
```

---

## ⚙️ Configuration
Le fichier `2-isolation/config.py` centralise les paramètres critiques.

### Paramètres Principaux
| Paramètre | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `REDIS_HOST` | Adresse du serveur Redis | `localhost` |
| `REDIS_PORT` | Port Redis | `6379` |
| `OLLAMA_API_URL` | Endpoint Ollama | `http://localhost:11434/api/generate` |
| `OLLAMA_MODEL_NAME` | Modèle LLM | `mistral:7b` |
| `EMBEDDING_MODEL_NAME` | Modèle embeddings | `multi-qa-mpnet-base-dot-v1` |
| `SIMILARITY_THRESHOLD` | Seuil RAG | `0.85` |
| `APPLICATIONS_IDS` | Mapping app_id vers nom | Voir `config.py` |

### Mappings des Applications
```python
APPLICATIONS_IDS = {
    1234567890: "Application_Recette",
    1234567891: "Application_Quran",
    1234567892: "Application_Qissas"
}
```

---

## 🧩 Architecture Logique

### 1. Chargement des Données (RAG)
Géré dans `load_application_data(app_id)` :
* Lecture des embeddings `.pt`.
* Lecture des documents `.json`.
* Mise en mémoire RAM pour accélérer les recherches.

### 2. Trouver le Contexte Pertinent
* Embedding de la question.
* Comparaison avec les embeddings existants.
* Filtrage selon le seuil de similarité.

### 3. Appel LLM ou Cache
Géré dans `ask_llm_with_redis_smart()` :
* Vérifie si la réponse existe déjà dans Redis.
* Sinon, prépare un prompt enrichi.
* Appelle Ollama pour la génération.
* Stocke la réponse dans Redis.

---

## 🌐 API REST
Le service expose un seul endpoint principal.

### `POST /ask`
Permet de poser une question dans un contexte donné.

#### Corps JSON
```json
{
  "app_id": 1234567891,
  "question": "Quel est le nom de la première sourate du Coran ?"
}
```

#### Réponse Exemple
```json
{
  "response": "La première sourate du Coran est Al-Fatiha.",
  "source": "LLM RAG"
}
```

`source` peut être :
* `Cache Redis`
* `LLM RAG`

---

## ▶️ Lancer l'API

### Prérequis
* Python 3.x
* Redis en local ou distant
* Ollama installé avec `mistral:7b`

### Installation
```bash
pip install fastapi uvicorn pydantic python-dotenv redis
```

### Démarrage
```bash
python 2-isolation/api.py
```
Serveur disponible sur : `http://0.0.0.0:8000`

---

## 📦 Ajout de Nouvelles Applications RAG
1. Placer un nouveau fichier embeddings dans `/data`.
2. Placer son fichier textuel JSON dans `/data`.
3. Ajouter l'entrée dans `APPLICATIONS_IDS`.
4. Redémarrer le serveur.

Le système est automatiquement extensible.

---

## ✔️ Avantages
* Réponses précises et contextualisées.
* Latence minimale grâce au caching.
* Architecture claire et maintenable.
* Scalabilité horizontale par application.

