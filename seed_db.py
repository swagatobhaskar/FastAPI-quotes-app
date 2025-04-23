import os
from database import engine, SessionLocal
from models import Base, Quote

# wipe clean each time, optional
# Base.metadata.drop_all(bind=engine)

ENV = os.getenv("ENV", "development")

# Create tables in development (if they don't exist yet)
if ENV == "development":
    Base.metadata.create_all(bind=engine)

# Add seed data
db = SessionLocal()


if ENV == "development":
    # Check if the database already has quotes
    quote_count = db.query(Quote).count()

    if quote_count == 0:
        print("** No quote found! Seeding Database..")

        quotes = [
            Quote(id=1, author='bob', text='Awwwu..'),
            Quote(id=2, author='john hoe', text='I\'m gay'),
            Quote(
                id=3,
                author='bruce lee',
                text='Don\'t pray for an easy life, pray for the endurance to live a hard life.'
            ),
            Quote(
                id=4,
                author='marie curie',
                text='Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, \
                    so that we may fear less.'
            )
        ]
        
        db.add_all(quotes)
        db.commit()
        print("✅️ Seeded test.db with sample quotes.")

    else:
        print(f"⚠️  Database already has {quote_count} quote(s). Skipping seed.")

else:
    print("⚠️ Skipping seed in non-dev environment.")

db.close()
