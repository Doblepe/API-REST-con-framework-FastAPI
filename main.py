from fastapi import FastAPI, Request, Form
import pandas as pd
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import csv
from models import iris
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
MEDIA_ROOT = "iris.csv"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    df = pd.read_csv(MEDIA_ROOT, header=None)
    array = df.to_numpy()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": array,
        "message": "Hola gente, vamos a usar FastAPI",
        "explanation": "The data is: "
    })

@app.post("/insertData/")
async def insertData(item: iris):

    with open(MEDIA_ROOT, 'a', newline='') as csvfile:
        fieldname = ['sepal_length','sepal_width','petal_length','petal_width','species']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writerow({'sepal_length': item.sepal_length,'sepal_width': 
        item.sepal_width,'petal_length': item.petal_length,
        'petal_width':item.petal_width,'species': item.species})
        return item

@app.put("/updateData/{item_id}")
async def updateData(item_id: int, item: iris):
    df = pd.read_csv(MEDIA_ROOT)
    df.loc[df.index[-1], 'sepal_length']= item.sepal_length
    df.loc[df.index[-1], 'sepal_width']= item.sepal_width
    df.loc[df.index[-1], 'petal_length']= item.petal_length
    df.loc[df.index[-1], 'petal_width']= item.petal_width
    df.loc[df.index[-1], 'species']= item.species
    df.to_csv(MEDIA_ROOT, index=False)
    return {"item_id": item_id, **item.dict()}

@app.delete("/deletData/")
async def deleteData():
    df = pd.read_csv(MEDIA_ROOT)
    df.drop(df.index[-1], implace = True)
    df.to_csv(MEDIA_ROOT, index=False)
    return "Eliminado"