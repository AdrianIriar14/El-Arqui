import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"¿Clave cargada?: {key is not None}")
if key:
    genai.configure(api_key=key)
    # Listar modelos disponibles
    for m in genai.list_models():
        print(f"Modelo disponible: {m.name}")
