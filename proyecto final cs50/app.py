import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from cs50 import SQL

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

    try:
        # LEER TODOS LOS ÍTEMS (Ahora incluimos el ID)
        items_db = db.execute("SELECT id, categoria, nombre, unidad, precio_unitario FROM items_construccion")

        catalogo_ia = []
        for item in items_db:
            catalogo_ia.append({
                "id": item["id"],
                "nombre": item["nombre"],
                "unidad": item["unidad"]
            })

        prompt = f"""
        Actúa como un Arquitecto e Ingeniero Civil experto que trabaja en Santa Cruz de la Sierra, Bolivia.
        Analiza esta imagen de una fachada o plano y estima las cantidades necesarias para su construcción.
        Toma en cuenta el contexto cruceño: clima cálido, lluvias, métodos constructivos locales y el uso frecuente de ladrillo y hormigón armado.

        REGLAS MATEMÁTICAS ESTRICTAS:
        1. Estima los metros cuadrados (m2) totales de construcción visibles.
        2. Calcula cantidades realistas para cada ítem de nuestro catálogo basándote en esos m2.
        3. Para el tiempo de entrega: calcula 1 semana por cada 15 m2 estimados (número entero).

        CATÁLOGO DISPONIBLE:
        {json.dumps(catalogo_ia, ensure_ascii=False, indent=2)}

        FORMATO DE RESPUESTA OBLIGATORIO:
        Devuelve ÚNICAMENTE un objeto JSON estructurado exactamente así:
        {{
            "tiempo_semanas": <entero>,
            "items": [
                {{"id": 1, "cantidad": <numero>}},
                {{"id": 2, "cantidad": <numero>}}
            ]
        }}
        Incluye en la lista "items" solo aquellos IDs que requieran una cantidad mayor a 0. No agregues texto fuera del JSON.
        """

        config = genai.types.GenerationConfig(
            temperature=0.0,
            response_mime_type="application/json"
        )

        response = model.generate_content(
            contents=[prompt, {"mime_type": "image/jpeg", "data": image_data}],
            generation_config=config
        )

        if not response.text:
            return jsonify({"error": "La IA no devolvió respuesta"}), 500

        print("Respuesta de IA cruda:", response.text)
        datos_ia = json.loads(response.text)

        total_materiales = 0
        total_acabados = 0
        total_mano_obra = 0
        tiempo = datos_ia.get("tiempo_semanas", 4)

        # Convertir la lista de la IA en un diccionario para búsqueda rápida { id_item: cantidad }
        cantidades_por_id = { item["id"]: item["cantidad"] for item in datos_ia.get("items", []) }


        for item in items_db:
            item_id = item['id']
            categoria = item['categoria']
            precio_unitario = float(item['precio_unitario'])

            cantidad_estimada = float(cantidades_por_id.get(item_id, 0))
            costo_total_item = cantidad_estimada * precio_unitario

            if categoria == 'Material Base':
                total_materiales += costo_total_item
            elif categoria == 'Acabado':
                total_acabados += costo_total_item
            elif categoria == 'Mano de Obra':
                total_mano_obra += costo_total_item

        return jsonify({
            "materiales": round(total_materiales, 2),
            "mano_obra": round(total_mano_obra, 2),
            "acabados": round(total_acabados, 2),
            "tiempo": tiempo
        })

    except Exception as e:
        print("ERROR DETECTADO:", str(e))
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
