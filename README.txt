Nombre del proyecto:
El Arqui - Calculadora de presupuestos para arquitectura con IA

Descripción:
Aplicación web diseñada para estimar costos de construcción de viviendas en Santa Cruz de la Sierra. El sistema utiliza inteligencia artificial para analizar imágenes de planos de fachadas y estimar presupuestos necesarios para su construccion, cruzando esta información con una base de datos relacional local para calcular el costo financiero exacto de materiales, mano de obra y acabados de forma determinística.

Integrantes:
Adrian Pachajaya Iriarte
Fabian Serrano Catari
Erick Jhon Nava Cueto
German Cesar Lozano Maldonado

Lenguaje utilizado:
Python 3 (Backend) y JavaScript, HTML5, CSS3 (Frontend)

Base de datos utilizada:
SQLite3 mediante la librería cs50.SQL

Archivo principal:
app.py Controlador principal del servidor Flask

Requisitos de instalación:
1. Python 3.x instalado en el sistema
2. Librerías de Python: pip install flask, cs50, google-generativeai, python-dotenv.
3. Una clave válida de la API de Google Gemini (gemini-2.5-flash).
4. Navegador web actualizado para ejecutar el cliente frontend.

Pasos para ejecutar:
1. Abrir la carpeta del proyecto en la terminal
2. Verificar que el entorno virtual esté activo y todas las dependencias instaladas
3. Crear un archivo llamado ".env" en la raíz del proyecto y agregar la variable: GEMINI_API_KEY="Colocar API KEY de gemini aqui (sin comillas)"
4. Verificar que el archivo de base de datos "arqui.db" se encuentre en el mismo directorio
5. Ejecutar el servidor iniciando el archivo principal mediante el comando: flask run
6. Abrir el navegador web e ingresar a la dirección local: (puede ser) https://scaling-fishstick-xrw7jg9664763vwxp-5000.app.github.dev

Datos de prueba:
- Imagen de prueba: Cualquier fotografía clara con plano 2D de una de casa

Funcionalidades:
- Análisis visual automatizado de planos arquitectónicos o bocetos mediante IA
- Estimación estructurada en formato JSON de cantidades de obra.
- Cálculo financiero preciso separando costos por Materiales, Mano de Obra y Acabados.
- Interfaz asíncrona que muestra resultados sin recargar la página.

Limitaciones conocidas:
- El modelo actual está optimizado para analizar fachadas bidimensionales; no procesa cálculos estructurales complejos ni renders 3D.
- El sistema requiere una conexión a internet activa para comunicarse con el motor de Google Gemini.
- Los precios utilizados provienen de la base de datos local y son estáticos; no se actualizan en tiempo real con el mercado a menos que se modifiquen mediante sentencias SQL.
