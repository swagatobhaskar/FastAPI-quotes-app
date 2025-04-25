from typing import Union
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine

app = FastAPI()

allowed_origins = [
    "http://localhost:8000",
    "192.168.0.102", # local ubuntu
    "202.8.112.251", # public ip
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add Dependency to Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name= "static")

templates = Jinja2Templates(directory="templates")


@app.middleware('http')
async def log_client_ip(request: Request, call_next):
    client_ip = request.client.host
    print(f"Client IP: {client_ip}")

    response = await call_next(request)
    return response

@app.get("/root")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/",
         response_class=HTMLResponse,
         response_model=list[schemas.QuoteOut]
         )
def get_all_quotes(request: Request, db: Session = Depends(get_db)):
    all_quotes = db.query(models.Quote).all()

    return templates.TemplateResponse(
        request=request,
        name="quotes.html",
        context={"quotes": all_quotes}
    )


@app.get("/api/all-quotes", response_model=list[schemas.QuoteOut])
def get_all_quotes(db: Session = Depends(get_db)):
    all_quotes = db.query(models.Quote).all()
    return all_quotes

@app.post("/api/new-quote")
def add_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    new_quote = models.Quote(author=quote.author, text=quote.text)
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote
