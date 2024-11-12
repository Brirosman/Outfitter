import google.generativeai as genai
import urllib3
import requests






urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = 'acc_3798ba95def9b0d'
api_secret = '2a604eae7c4db9e8868f22ba49960559'

image_path = 'C:/Users/48793373/Documents/Outfitter/IA/Fotos/river.jpg'



def analyze_image(image_path):
    tags, extracted_texts, color_info = [], [], []

    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(api_key, api_secret),
            files={'image': image_file},
            verify=False
        )
    tags = response.json()
    nombre_posta = [tag['tag']['en'] for tag in tags['result']['tags'] if tag['confidence'] > 15]
   
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.imagga.com/v2/text',
            auth=(api_key, api_secret),
            files={'image': image_file},
            verify=False
        )
    text_data = response.json()
                

    if 'result' in text_data and 'text' in text_data['result']:
        extracted_texts = [item['data'] for item in text_data['result']['text']]
         

    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.imagga.com/v2/colors',
            auth=(api_key, api_secret),
            files={'image': image_file},
            verify=False
        )
    colors = response.json()
    dominant_colors = colors.get('result', {}).get('colors', {}).get('image_colors', [])
    colores_prenda = [
        (color.get('closest_palette_color'), color.get('closest_palette_color_parent'))
        for color in dominant_colors
    ]

    return nombre_posta, extracted_texts, colores_prenda

tags, texts, colors = analyze_image(image_path)

#  Gemini API
api_key = 'AIzaSyA64bLOsQ0jjQPAkmHCdL8NwaQZWRIQhDk'
genai.configure(api_key=api_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,

)

instruccion_gemino = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Vas a recibir información sobre una imagen que muestra una prenda de ropa o accesorio. Tu trabajo es hacer una búsqueda en Google para encontrar dónde comprarla, usando una frase simple. Aquí te explico qué hacer:\n\n1. Ropa: Fíjate en qué tipo de prenda aparece en la imagen (camiseta, pantalón, sombrero, etc.) y describe la prenda con detalles.\n\n2. Colores: Observa los colores de la prenda y di cuáles son. Asegúrate de identificar al menos dos colores.\n\n3. Texto Extraído: Si hay palabras en la prenda, escríbelas exactamente como están.\n\nCon esta información, haz una búsqueda en Google usando solo la frase:\n\"comprar [tipo de prenda] [color 1] [color 2] [texto extraído] online\"."
            ],
        },
       
    ]
)




input_data = f"{tags}\n"
if texts:
    input_data += f"Texto extraído: {' '.join(texts)}\n"
for color_name, color_parent in colors:
    input_data += f"Color: {color_name}, Parent Color: {color_parent}\n"

response = instruccion_gemino.send_message(input_data)

candidates = response.candidates
content = candidates[0].content
parts = content.parts
text = parts[0].text
text = text.strip('"')
print(text)








#Serp API
import requests
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

query = text

def google_search(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": "17791f133d05bd9e5629260faf196e641e395e087849f32e0361e416956ddb27",
        "safe":"active",
        "hl":"es",
        "gl": "ar",
        "location": "Argentina",

    }

    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        return f"Error 9/12 {e}"

    return response.json().get('organic_results', [])

resultados = google_search(text)

for result in resultados:
  print(result['title'])
  print(result['link'])
  print(result['snippet']) 
  print('-' * 50)

# input_analyzer = [(result['link'], result['title'], result['snippet']) for result in resultados]


# THE ANALYZER 

# import requests
# import os
# import google.generativeai as genai

# api_key2 = 'AIzaSyBFJdYALbfs0cHffT-tE-gYB_k4N0idGOQ'
# genai.configure(api_key=api_key2)

# generation_config_analyzer = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model_analyzer = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config_analyzer,
#     system_instruction="""
#     Task introduction:
#     Tu tarea es evaluar la relevancia y precisión de los resultados de búsqueda de ropa basada en una imagen. Se te dará enlaces generados por una búsqueda en Google, y debes calificarlo de acuerdo con criterios como la calidad de la descripción de la prenda y si es relevante para la ropa identificada.

#     Evaluation criteria:
#     Evalúa los siguientes enlaces obtenidos de una búsqueda en Google para la prenda.
#     - Precisión: ¿El enlace lleva a una tienda o página donde realmente se puede comprar la prenda detectada?
#     - Relevancia: ¿El enlace está relacionado directamente con la prenda?
#     - Popularidad: ¿El enlace lleva a un sitio confiable o conocido?

#     Proporciona un puntaje de 0 al 1 para cada criterio y una breve explicación.

#     Evaluation steps:
#     Tu tarea es evaluar la relevancia y precisión de los resultados de búsqueda de ropa basada en una imagen. A continuación, se te proporcionarán enlaces obtenidos de una búsqueda en Google, y deberás evaluarlos según los siguientes criterios:

#    Criterios de Evaluación:
#    Precisión:

#     ¿El enlace lleva a una tienda o página donde realmente se puede comprar la prenda identificada en la imagen?
#  Puntaje: 0 (no es posible comprar la prenda) a 1 (la prenda exacta está disponible para la compra).
#  Relevancia:

#  ¿El enlace está directamente relacionado con la prenda identificada?
#  Puntaje: 0 (el enlace es irrelevante o muestra productos diferentes) a 1 (el enlace muestra exactamente la prenda o productos altamente relacionados).
#  Popularidad:

#  ¿El enlace lleva a un sitio web confiable o conocido?
#  Puntaje: 0 (el sitio parece poco confiable o sospechoso) a 1 (el sitio es popular y confiable, como Amazon, Zara, etc.).

#   Formato de Evaluación:
#  Para cada enlace, proporciona una puntuación de 0 a 1 en cada uno de los tres criterios y acompáñala con una breve explicación justificando tu decisión.

#  Ejemplo de Evaluación:

#  Enlace 1: [URL]

#  Precisión: 0.8 - La prenda es similar a la de la imagen, pero con pequeñas diferencias en el diseño.
#  Relevancia: 1 - El enlace está directamente relacionado con la prenda buscada.
#  Popularidad: 1 - El sitio web es ampliamente conocido y confiable.
#  Notas Finales:
#  Después de evaluar todos los enlaces, promedia los puntajes de los tres criterios para cada enlace.
#  Proporciona un resumen final sobre la calidad general de los resultados de la búsqueda.
#  """
# )

# analyzer_chat = model_analyzer.start_chat()
# for result in resultados:
#     if isinstance(result, dict):
#         titulo = result.get('title', 'Título no disponible')
#         enlace = result.get('link', 'Enlace no disponible')
#         snippet = result.get('snippet', 'Descripción no disponible')

#         input_data_analyzer = f"""
#         El enlace proporcionado es: {enlace}.
#         Título del enlace: {titulo}.
#         Descripción del enlace: {snippet}.
#         Texto extraído: {' '.join(texts)}.
#         Colores identificados en la prenda:
#         """
#         for color_name, color_parent in colors:
#             input_data_analyzer += f"- Color: {color_name}, Parent Color: {color_parent}\n"

    

#         response_analyzer = analyzer_chat.send_message(input_data_analyzer)
   

#         evaluacion = response_analyzer.candidates[0].content
#     #     print(f"Evaluación del enlace: {enlace}\n{evaluacion}\n{'-' * 50}")
#     # else:
#         # print("El resultado no es un diccionario válido.")
       
   