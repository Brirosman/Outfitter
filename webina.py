from typing import Union
from funka import *
from index import *
from links import *
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/upload/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_path = f"./uploads/{file.filename}"  
    with open(image_path, "wb") as image:
        content = await file.read()
        image.write(content)

    tags, texts, colors = analyze_image(image_path)

    return {"tags": tags, "texts": texts, "colors": colors}

