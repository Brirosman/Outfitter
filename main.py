from fastapi import FastAPI
import uvicorn
from typing import Union
import google.generativeai as genai
import urllib3
import requests
import cloudinary
import cloudinary.uploader
from fastapi import FastAPI, File, UploadFile
import os
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Permite todos los orígenes (ajusta según sea necesario)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)




app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.mount("/media", StaticFiles(directory="media"), name="media")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cloudinary.config(
    cloud_name="dtb2lrzet",
    api_key="475625168932265",
    api_secret="QRZneD3fqb8G1vpNnMJ5JofE_MA"
)




@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/links.html", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("links.html", {"request": request})




image_url = None

class SecureURLRequest(BaseModel):
    secure_url: str



@app.post("/get-link")
async def get_link(request: SecureURLRequest):
    global image_url
    image_url = request.secure_url  
    print("URL recibida:", image_url)
    return {"message": "URL recibida correctamente", "image_url": image_url}

@app.get("/analizar/")
async def analizar():
    try:
        print("Inicio del análisis...")

        # Validar si la URL de la imagen está disponible
        global image_url
        if not image_url:
            return {"error": "No se ha proporcionado ninguna URL para analizar"}

        # Configuración de credenciales para Imagga
        api_key = 'acc_3798ba95def9b0d'
        api_secret = '2a604eae7c4db9e8868f22ba49960559'

        # Función para analizar la imagen
        def analyze_image(image_url):
            tags, extracted_texts, colores_prenda = [], [], []

            # Obtener etiquetas de la imagen
            try:
                response = requests.get(
                    f'https://api.imagga.com/v2/tags?image_url={image_url}',
                    auth=(api_key, api_secret), verify=False
                )
                response.raise_for_status()
                tags_data = response.json()
                tags = [tag['tag']['en'] for tag in tags_data['result']['tags'] if tag['confidence'] > 15]
            except Exception as e:
                print(f"Error al obtener etiquetas: {e}")
                tags = []

            # Extraer texto de la imagen
            try:
                response = requests.get(
                    f'https://api.imagga.com/v2/text?image_url={image_url}',
                    auth=(api_key, api_secret), verify=False
                )
                response.raise_for_status()
                text_data = response.json()
                extracted_texts = [item['data'] for item in text_data.get('result', {}).get('text', [])]
            except Exception as e:
                print(f"Error al extraer texto: {e}")
                extracted_texts = []

            # Obtener colores dominantes
            try:
                response = requests.get(
                    f'https://api.imagga.com/v2/colors?image_url={image_url}',
                    auth=(api_key, api_secret), verify=False
                )
                response.raise_for_status()
                colors_data = response.json()
                dominant_colors = colors_data.get('result', {}).get('colors', {}).get('image_colors', [])
                colores_prenda = [
                    (color.get('closest_palette_color'), color.get('closest_palette_color_parent'))
                    for color in dominant_colors
                ]
            except Exception as e:
                print(f"Error al analizar colores: {e}")
                colores_prenda = []

            return tags, extracted_texts, colores_prenda

        # Llamar a la función para analizar la imagen
        tags, texts, colors = analyze_image(image_url)
        print("Análisis completado:", tags, texts, colors)

        # Configuración de GenAI
        genai_api_key = 'AIzaSyA64bLOsQ0jjQPAkmHCdL8NwaQZWRIQhDk'
        genai.configure(api_key=genai_api_key)

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

        # Preparar el mensaje para GenAI
        input_data = f"{tags}\n"
        if texts:
            input_data += f"Texto extraído: {' '.join(texts)}\n"
        for color_name, color_parent in colors:
            input_data += f"Color: {color_name}, Parent Color: {color_parent}\n"

        instruccion_gemino = model.start_chat(
            history=[{
                "role": "user",
                "parts": [
                    "Vas a recibir información sobre una imagen que muestra una prenda de ropa o accesorio. "
                    "Tu trabajo es hacer una búsqueda en Google para encontrar dónde comprarla, usando una frase simple."
                ],
            }]
        )
        response = instruccion_gemino.send_message(input_data)
        content = response.candidates[0].content.parts[0].text.strip('"')
        print("Respuesta de GenAI:", content)
        
            # Realizar la búsqueda en Google
        resultados = google_search(content)
        
            # Verificar si hay resultados
        if not resultados:
                print("No se encontraron resultados para la búsqueda.")
                return {"error": "No se encontraron resultados para la búsqueda de productos"}
        
            # Extraer los enlaces de los resultados
        links = [result['link'] for result in resultados]
        print("Enlaces encontrados:", links)
        
            # Devolver los enlaces encontrados
        return {"links": links}
        
    except Exception as e:
            print(f"Error general: {e}")
            return {"error": str(e)}
        
    def google_search(query):
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": "17791f133d05bd9e5629260faf196e641e395e087849f32e0361e416956ddb27",
            "safe": "active",
            "hl": "es",
            "gl": "ar",
            "location": "Argentina",
        }
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        
        # Imprimir la respuesta completa para ver qué está devolviendo
        print("Respuesta de SerpAPI:", response.json())
        
        return response.json().get('organic_results', [])