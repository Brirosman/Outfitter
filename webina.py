from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import subprocess 
from fastapi.responses import JSONResponse
from funka import analyze_image



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/links.html", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("links.html", {"request": request})

@app.post("/analizar/")
async def analyze_image (file: UploadFile = File(...)):
    contents = await file.read()
    with open("funka.py", "wb") as f:
        f.write(contents)
    result = subprocess.run(["python3", "funka.py"], capture_output=True, text=True)
    return JSONResponse(content={"output": result.stdout})