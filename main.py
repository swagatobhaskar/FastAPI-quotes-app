from typing import Union
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name= "static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/all-quotes", response_class=HTMLResponse)
async def get_all_quotes(request: Request):
    quotes = [
        {'id': 1, 'author': 'bob', 'text': 'Awwwu..'},
        {'id': 2, 'author': 'john hoe', 'text': 'I\'m gay'},
        {
            'id': 3, 'author': 'bruce lee',
            'text': 'Don\'t pray for an easy life, pray for the endurance to live a hard life.'
        }
    ]

    return templates.TemplateResponse(
        request=request,
        name="quotes.html",
        context={"quotes": quotes}
    )
