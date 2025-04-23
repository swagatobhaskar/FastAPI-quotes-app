from database import engine, SessionLocal
from models import Base, Quote

# wipe clean each time, optional
# Base.metadata.drop_all(bind=engine)

# Create tables (if they don't exist yet)
Base.metadata.create_all(bind=engine)

# Add seed data
db = SessionLocal()

# Check if the database already has quotes
quote_count = db.query(Quote).count()

if quote_count == 0:
    print("** No quote found! Seeding Database..")

    quotes = [
        {'id': 1, 'author': 'bob', 'text': 'Awwwu..'},
        {'id': 2, 'author': 'john hoe', 'text': 'I\'m gay'},
        {'id': 3, 'author': 'bruce lee', 'text': 'Don\'t pray for an easy life, pray for the endurance to live a hard life.'}
        ]

    db.add_all(quotes)
    db.commit()
    print("Seeded test.db with sample quotes.")

else:
    print(f"⚠️  Database already has {quote_count} quote(s). Skipping seed.")

db.close()
