from typing import Union
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, database, schemas
from database import SessionLocal

app = FastAPI()

# Add Dependency to Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="static"), name= "static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/all-quotes",
        #  response_class=HTMLResponse,
        response_model=list[schemas.QuoteOut]
        )
def get_all_quotes(
        # request: Request, 
        db: Session = Depends(get_db)
    ):
    # quotes = [
    #     {'id': 1, 'author': 'bob', 'text': 'Awwwu..'},
    #     {'id': 2, 'author': 'john hoe', 'text': 'I\'m gay'},
    #     {
    #         'id': 3, 'author': 'bruce lee',
    #         'text': 'Don\'t pray for an easy life, pray for the endurance to live a hard life.'
    #     }
    # ] 
    all_quotes = db.query(models.Quote).all()
    return all_quotes

    # return templates.TemplateResponse(
    #     request=request,
    #     name="quotes.html",
    #     context={"quotes": all_quotes}
    # )

@app.post("/new-quote")
def add_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    new_quote = models.Quote(author=quote.author, text=quote.text)
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote
