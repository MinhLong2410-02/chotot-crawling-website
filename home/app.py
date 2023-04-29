from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run
import requests as req
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}, status_code=200)

@app.post("/price_range")
async def get_price_range(request, min_price: int = Form(...), max_price: int = Form(...)):
    data = req.get("http://mysql_api:9002/price-range", params={"min_price": min_price, "max_price": max_price}).json()
    
    return templates.TemplateResponse("index.html", {"request": request, "result": data}, status_code=200)

@app.post("/phone")
async def get_phone(request, name: str = Form(...)):
    data = req.get("http://mysql_api:9002/phone", params={"subject_content": name}).json()
    return templates.TemplateResponse("index.html", {"request": request, "result": data}, status_code=200)

run(app, 
    host="0.0.0.0", 
    port=8000)
