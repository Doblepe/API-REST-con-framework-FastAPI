from fastapi import FastAPI, Request
import pandas as pd
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import csv
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
MEDIA_ROOT = 'iris.csv'

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hola gente, vamos a usar html con FastAPI",
        "explanation": "Bienvenido a FAST API, lección 9 del master en programación de python"
    })
    
# @app.get("/")
# async def root():
#     return 'Bienvenido a FastAPI'