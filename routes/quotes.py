from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

import models
import schemas
from dependencies import get_db

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/",
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

@router.get("/api/all-quotes", response_model=list[schemas.QuoteOut])
def get_all_quotes(db: Session = Depends(get_db)):
    all_quotes = db.query(models.Quote).all()
    return all_quotes

@router.post("/api/new-quote")
def add_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    new_quote = models.Quote(author=quote.author, text=quote.text)
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote
