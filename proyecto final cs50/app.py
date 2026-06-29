import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from cs50 import SQL

# Configuración inicial
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inicialización
app = Flask(__name__)
db = SQL("sqlite:///arqui.db")
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analizar", methods=["POST"])
def analizar_presupuesto():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    file = request.files['file']
    image_data = file.read()

    prompt = """
    Imagina que eres un arquitecto profesional y analiza esta imagen de una fachada de construcción. Estima los costos totales
    para una obra de estas características en Bolivia, analiza y haz una estimacion de todas lo necesario para culminar esta obra.
    Devuélveme exclusivamente un JSON con estos valores estimados:
    {"materiales": <valor_calculado>, "mano_obra": <valor_calculado>, "acabados": <valor_calculado>, "tiempo": <semanas>}
    Basado en el estilo visual de la imagen, calcula tú los valores aproximados.
    No escribas texto extra, solo el JSON.
    """

    try:
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])

        if not response.text:
            return jsonify({"error": "La IA no devolvió respuesta"}), 500

        texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
        print("Respuesta cruda de IA:", texto_limpio)

        datos_json = json.loads(texto_limpio)
        return jsonify(datos_json)

    except Exception as e:
        print("ERROR DETECTADO:", str(e))
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
