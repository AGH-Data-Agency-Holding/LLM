# Server Utils - LLM Service Module

## Overview
`server_utils.py` is the core application logic file for a multilingual RAG (Retrieval-Augmented Generation) system with smart caching capabilities. It integrates Redis caching, sentence embeddings, and LLM services (Ollama/Gemini) to provide contextual responses based on application-specific data.

## Features
- **Application-specific RAG**: Loads embeddings and prompts for different applications
- **Smart Redis Caching**: Caches similar questions using cosine similarity threshold
- **Multi-LLM Support**: Supports both Ollama (local) and Gemini (cloud) LLMs
- **Embedding-based Retrieval**: Uses Sentence Transformers for semantic similarity
- **Streaming Responses**: Handles streaming responses from Ollama API

## Dependencies
- `torch`: For tensor operations and embedding storage
- `redis`: For caching and similarity lookup
- `sentence-transformers`: For text embeddings
- `requests`: For API calls to Ollama
- `google-genai`: For Gemini API integration
- `config`: Application configuration
- `prompts`: Application-specific prompts

## Key Functions

### `load_application_data(app_id: int)`
Loads RAG data and prompts for a specific application ID. Returns `True` if successful.

### `ask_llm_with_redis_smart(question: str, app_id: str)`
Main entry point that:
1. Checks Redis cache for similar questions
2. If found, returns cached response
3. Otherwise, retrieves relevant context and calls LLM
4. Caches the new response

### `automate_asking(query: str)`
Orchestrates context retrieval and LLM calling for uncached queries.

### `find_similar_question(query_emb, app_id)`
Searches Redis for similar questions using cosine similarity threshold.

## Usage Example
```python
from server_utils import load_application_data, ask_llm_with_redis_smart

# Load application data
app_id = 1234567892
load_application_data(app_id=app_id)

# Ask a question
response, from_cache = ask_llm_with_redis_smart(
    "quelle est l'histoire de prophet mohamed", 
    app_id=str(app_id)
)
```
## Configuration et Notes d'Utilisation

Ce document décrit les exigences de configuration et les notes importantes concernant l'utilisation de l'application.

---

## ⚙️ Configuration Requise

Un paramétrage correct est **obligatoire** dans le fichier `config.py`. Les éléments suivants doivent être spécifiés :

* **Paramètres de connexion Redis** : Les détails nécessaires pour établir la connexion à la base de données Redis.
* **Nom du modèle d'embedding** : Le nom du modèle à utiliser pour la génération des embeddings.
* **Endpoints LLM (Ollama/Gemini)** : Les adresses des points de terminaison pour les modèles de langage (Large Language Models) pris en charge (par exemple, via Ollama ou l'API Gemini).
* **Mappage des ID d'application** : Une correspondance définissant les identifiants pour chaque application.
* **Chemins d'accès aux données** : Les chemins menant aux ressources de données nécessaires.

---

## 📝 Notes Importantes

* **Variables Globales** : Le code utilise des **variables globales** pour les embeddings et les invites (`prompts`).
* **Sécurité des Threads** : L'application est considérée comme **thread-safe** dans le contexte d'une **application unique**.
* **Embeddings Pré-calculés** : L'utilisation nécessite que les embeddings soient **pré-calculés** et stockés au format `.pt`.
* **Prise en Charge des Appareils** : Le système prend en charge l'utilisation des dispositifs **CPU** et **GPU**.


