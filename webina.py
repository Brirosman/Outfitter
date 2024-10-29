from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io

app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/links.html", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("links.html", {"request": request})





@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    message = process_image(image)
    return templates.TemplateResponse("links.html", {"request": request, "message": message})




def process_image(image: Image.Image) -> str:
    # Implement your image processing logic here
    return "Image processed successfully"