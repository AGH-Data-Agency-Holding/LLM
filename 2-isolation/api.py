# ========================================
# api.py
# API REST FastAPI pour le service LLM
# ========================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

try:
    from server_utils_optimised import load_application_data, ask_llm_with_redis_smart
    from config import APPLICATIONS_IDS
except ImportError as e:
    print(f"Erreur d'importation des utilitaires du serveur: {e}")
    pass


app = FastAPI(
    title="LLM RAG & Caching API",
    description="Service de Réponse LLM avec RAG et mise en cache Redis (Thread-Safe).",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    """Schéma pour la requête utilisateur."""
    app_id: int
    question: str


# --- Endpoint principal de l'API ---
@app.post("/ask", response_model=Dict[str, str])
async def ask_llm(request: QueryRequest):
    """
    Traite la question de l'utilisateur, charge le contexte RAG par ID 
    si nécessaire, et utilise le cache intelligent.
    """
    app_id = request.app_id
    question = request.question

    if app_id not in APPLICATIONS_IDS:
        raise HTTPException(
                    status_code=400, 
                    detail=f"L'ID d'application {app_id} est inconnu."
        )
    
    if not load_application_data(app_id):
        raise HTTPException(
            status_code=500, 
            detail=f"Échec de l'initialisation des données RAG pour l'application ID: {app_id}."
        )

    try:
        response_text, from_cache = ask_llm_with_redis_smart(
            question=question, 
            app_id=str(app_id) 
        )

        return {
            "response": response_text,
            "source": "Cache Redis" if from_cache else "LLM RAG"
        }

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Erreur de runtime du service : {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur interne s'est produite : {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)