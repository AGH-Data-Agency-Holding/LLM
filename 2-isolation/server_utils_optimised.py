# ========================================
# server_utils.py
# ========================================


import os
import torch
import redis
import json
import requests
from sentence_transformers import SentenceTransformer, util
from google import genai


# Importation des Configurations
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB, OLLAMA_API_URL, 
    EMBEDDING_MODEL_NAME, SIMILARITY_THRESHOLD, OLLAMA_MODEL_NAME, 
    DATA_PATH, APPLICATIONS_IDS, API_KEY, DEVICE
)
from prompts import PROMPTS_BY_APPLICATIONS

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    r.ping()
except redis.exceptions.ConnectionError as e:
    print(f"❌ Erreur de connexion Redis : {e}")

try:

    GLOBAL_EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME, device=DEVICE)
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle SentenceTransformer: {e}")

APP_CONTEXT_CACHE = {} 


# ========================================
# Fonctions de Service (Logique)
# ========================================

def load_application_data(app_id: int):
    """
    Charge les données RAG et le prompt spécifique à l'application dans un cache global.
    Si déjà en cache, retourne True immédiatement (Thread-Safe).
    """
    
    if app_id not in APPLICATIONS_IDS:
        return False

    if app_id in APP_CONTEXT_CACHE:
        return True

    application_name = APPLICATIONS_IDS[app_id]
    file_name = application_name.lower().replace("application_", "") + "_embeddings.pt"
    full_data_path = os.path.join(DATA_PATH, file_name)
    
    try:
        data_loaded = torch.load(
            full_data_path,
            map_location=torch.device(DEVICE)
            )
        
        # 2. Stockage dans le dictionnaire, lié à l'app_id.
        APP_CONTEXT_CACHE[app_id] = {
            "embeddings": data_loaded["embeddings"],
            "texts": data_loaded["texts"],
            "prompt_template": PROMPTS_BY_APPLICATIONS[application_name]
        }
        
        return True

    except Exception as e:
        print(f"❌ Erreur inconnue lors du chargement des données : {e}")
        return False


def get_application_context(app_id: int):
    """
    Fonction utilitaire pour récupérer le contexte RAG d'une application
    dans le cache.
    """
    if app_id not in APP_CONTEXT_CACHE:
        raise RuntimeError(f"Le contexte RAG pour l'ID {app_id} n'a pas été chargé.")
    return APP_CONTEXT_CACHE[app_id]

def gemini_response(prompt: str):
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def llm_response(prompt: str):
    stop_sequences = ["[STOP_GENERATION]"]

    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "stop": stop_sequences,  
        "options": {
            "temperature": 0.0
        }
    }

    # print("Payload envoyé à Ollama:")
    # print(json.dumps(payload, indent=2))  # Debug obligatoire

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        generated_text = data.get("response", "").strip()

        for seq in stop_sequences:
            if seq in generated_text:
                generated_text = generated_text.split(seq)[0].strip()

        return generated_text

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur avec Ollama: {e}")


def prompt_formatter(query: str, context_items: list[str], prompt_template: str) -> str:
    """
    Formate le prompt en utilisant le template fourni (argument, non global).
    """
    context = "- " + "\n- ".join(context_items) if context_items else "Aucune donnée disponible"
    
    base_prompt = prompt_template.format(
        context=context,
        query=query
    )
    print(base_prompt)
    return base_prompt


def retrieve_relevant_resources(query: str, embeddings, texts, n_resources_to_return: int = 5):
    """
    Récupère les ressources pertinentes du RAG en utilisant les données
    fournies en argument (embeddings et texts, non globaux).
    """
    
    query_embedding = GLOBAL_EMBEDDING_MODEL.encode(query, convert_to_tensor=True)

    dot_scores = util.dot_score(query_embedding, embeddings)[0]

    scores, indices = torch.topk(dot_scores, k=n_resources_to_return)

    relevant_texts = [texts[i] for i in indices.tolist()]
    return relevant_texts


def automate_asking_with_context(query: str, app_id: int):
    """
    Orchestre la récupération de contexte et l'appel LLM, en utilisant
    le contexte de l'application récupéré du cache.
    """
    
    context_data = get_application_context(app_id)
    embeddings = context_data["embeddings"]
    texts = context_data["texts"]
    prompt_template = context_data["prompt_template"]

    context_items = retrieve_relevant_resources(
        query=query, 
        embeddings=embeddings, 
        texts=texts
    )

    prompt = prompt_formatter(
        query=query, 
        context_items=context_items,
        prompt_template=prompt_template
    )
    
    return llm_response(prompt)
    # return gemini_response(prompt)

def get_embedding(text: str):
    """Utilise le modèle global chargé une seule fois."""
    return GLOBAL_EMBEDDING_MODEL.encode(text, convert_to_tensor=True)


def find_similar_question(query_emb, app_id):
    prefix = f"{app_id}:"

    for key in r.keys(f"{prefix}*"):
        raw = r.get(key)
        if not raw:
            continue  

        try:
            cached_data = json.loads(raw)
        except json.JSONDecodeError:
            continue  

        cached_emb = torch.tensor(cached_data["embedding"])
        similarity = util.cos_sim(query_emb, cached_emb).item()
        if similarity >= SIMILARITY_THRESHOLD:
            return key.decode(), cached_data["response"]

    return None, None



def ask_llm_with_redis_smart(question: str, app_id: str):
    """
    Fonction principale. L'orchestration du RAG est déléguée
    à automate_asking_with_context.
    """
    app_id_int = int(app_id) # Nécessaire pour l'appel interne au cache

    query_emb = get_embedding(question)

    similar_key, cached_response = find_similar_question(query_emb, app_id)

    if cached_response:
        return cached_response, True

    response_text = automate_asking_with_context(question, app_id_int) 

    cache_key = f"{app_id}:{question}"
    data_to_cache = {
        "embedding": query_emb.tolist(),
        "response": response_text
    }
    r.set(cache_key, json.dumps(data_to_cache))

    return response_text, False

r.flushall()
