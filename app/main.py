from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .middleware import log_client_ip
from .database import Base, engine
from .routes import quotes

app = FastAPI()

allowed_origins = [
    "http://localhost:8000",
    # "202.8.112.251", # public ip
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_client_ip)

# Create Database Tables
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name= "static")

app.include_router(quotes.router)

@app.get("/root")
def read_root():
    return {"message": "Hello, World!"}
