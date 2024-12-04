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




image_url = ""

class SecureURLRequest(BaseModel):
    secure_url: str


@app.post("/get-link")
async def get_link(request: SecureURLRequest):
    global image_url
    image_url = request.secure_url  
    print("URL recibida:", image_url)
    return {"message": "URL recibida correctamente", "image_url": image_url}


@app.get("/analizar")
async def read_root(image_url: str):
    
    api_key = 'acc_3798ba95def9b0d'
    api_secret = '2a604eae7c4db9e8868f22ba49960559'

    print("peli 1")  
    def analyze_image(image_url):
        
        tags, extracted_texts, color_info = [], [], []
        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
            auth=(api_key, api_secret),
            verify=False
        )
        
        tags = response.json()
        nombre_posta = [tag['tag']['en'] for tag in tags['result']['tags'] if tag['confidence'] > 15]

        response = requests.get(
            'https://api.imagga.com/v2/text?image_url=%s' % image_url,
            auth=(api_key, api_secret),
            verify=False
        )
        text_data = response.json()
        if 'result' in text_data and 'text' in text_data['result']:
            extracted_texts = [item['data'] for item in text_data['result']['text']]


            

        response = requests.get(
            'https://api.imagga.com/v2/colors?image_url=%s' % image_url,
            auth=(api_key, api_secret),
            verify=False
        )
        colors = response.json()
        dominant_colors = colors.get('result', {}).get('colors', {}).get('image_colors', [])
        colores_prenda = [
            (color.get('closest_palette_color'), color.get('closest_palette_color_parent'))
            for color in dominant_colors
        ]

        return nombre_posta, extracted_texts, colores_prenda

    print("algo cambio dentro de lotso")  
    tags, texts, colors = analyze_image(image_url)
    print("boop")  
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
        history=[{
            "role": "user",
            "parts": [
                "Vas a recibir información sobre una imagen que muestra una prenda de ropa o accesorio. "
                "Tu trabajo es hacer una búsqueda en Google para encontrar dónde comprarla, usando una frase simple. Aquí te explico qué hacer:\n\n"
                "1. Ropa: Fíjate en qué tipo de prenda aparece en la imagen (camiseta, pantalón, sombrero, etc.) y describe la prenda con detalles.\n\n"
                "2. Colores: Observa los colores de la prenda y di cuáles son. Asegúrate de identificar al menos dos colores.\n\n"
                "3. Texto Extraído: Si hay palabras en la prenda, escríbelas exactamente como están.\n\n"
                "Con esta información, haz una búsqueda en Google usando solo la frase:\n"
                "\"comprar [tipo de prenda] [color 1] [color 2] [texto extraído] online\"."
            ],
        }]
    )

    input_data = f"{tags}\n"
    if texts:
        input_data += f"Texto extraído: {' '.join(texts)}\n"
    for color_name, color_parent in colors:
        input_data += f"Color: {color_name}, Parent Color: {color_parent}\n"

    response = instruccion_gemino.send_message(input_data)
    print("pelota iconica")  
    candidates = response.candidates
    content = candidates[0].content
    parts = content.parts
    text = parts[0].text
    text = text.strip('"')
    print(text)

    query = text

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

        try:
            response = requests.get(url, params=params, verify=False)
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            return f"Error 9/12 {e}"

        return response.json().get('organic_results', [])

    resultados = google_search(text)
    print
    for result in resultados:
        print(result['title'])
        print(result['link'])
        print(result['snippet']) 
        print('-' * 50)

    links = [result['link'] for result in resultados]
    print(links)
    return {"Msg": links}
