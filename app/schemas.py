from pydantic import BaseModel

class QuoteCreate(BaseModel):
    author: str
    text: str

class QuoteOut(QuoteCreate):
    id: int
    author: str
    text: str

    class config:
        orm_mode= True
