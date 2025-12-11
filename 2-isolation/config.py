# ========================================
# config.py
# Fichier de configuration
# ========================================

import os
from dotenv import load_dotenv


# Paramètres du Service
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', "http://localhost:11434/api/generate")

# Paramètres du Modèle
EMBEDDING_MODEL_NAME = "multi-qa-mpnet-base-dot-v1"
SIMILARITY_THRESHOLD = 0.85
OLLAMA_MODEL_NAME = "mistral:7b"
DEVICE = 'cpu'

# Chemins
# Utilisation de os.path.expanduser pour une meilleure portabilité sur différents OS
BASE_DIR = "/home/ahmed/Desktop/AGH_Data_Agency_Holding_SA/Projet_LLM_Server/"
DATA_PATH = os.path.join(BASE_DIR, "data/") 

# Mappings des Applications
APPLICATIONS_IDS = {
    1234567890: "Application_Recette",
    1234567891: "Application_Quran",
    1234567892: "Application_Qissas"
}


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

