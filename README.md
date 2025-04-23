> ! Before running FastAPI server, seed the database by running `seed_db.py`. It will create and populate the database unless the database already exists.
>
> `>>> python seed_db.py`
>
> `>>> fastapi dev main.py`
>
> OR
>
>  `>>> uvicorn main:app --reload`

### Steps to Add SQLAlchemy
***
1. Install dependencies:
    
   e.g.  `pip install fastapi sqlalchemy uvicorn`

2. Create necessary files:
    ```
    ├── main.py
    ├── models.py
    ├── database.py
    └── schemas.py
    ```
3. Create the Database Connection in database.py.
4. Define Models in models.py.
5. Create Pydantic Schemas in schemas.py.
6. Create Database Tables:

    Somewhere early in your app (main.py):
    ```
    from . import models, database
    models.Base.metadata.create_all(bind=database.engine)
    ```
7. Add Dependency to Get DB Session:
    ```
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from .database import SessionLocal

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    ```
> That get_db() function is perfect for dependency injection in FastAPI routes — but it doesn't generate or manage migration files.
>
>  🚨 TL;DR:
>
> There are no migration files unless you use a migration tool like Alembic.

8.  Use Database in Endpoints.
   
