import os
from urllib.parse import urlparse
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_db
from app.database import Base

# use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# create schema once per test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Drop the existing tables
    Base.metadata.drop_all(bind=engine)
    # Create the test DB tables
    Base.metadata.create_all(bind=engine)

# Open a transaction for each test, and roll it back
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Override FastAPI dependency to use our test session
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # session closed in fixture

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# delete only if all tests pass — using a pytest hook.
# Extract path from URL (this strips 'sqlite:///' and gives './test.db')
parsed_url = urlparse(TEST_DATABASE_URL)
TEST_DB_PATH = parsed_url.path.lstrip('/')  # Removes leading slash on Linux/mac

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(exitstatus):
    # Delete test DB file if all tests passed
    if exitstatus == 0 and os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
        print(f"✅ Deleted {TEST_DB_PATH} after successful test run.")
    elif exitstatus != 0:
        print(f"⚠️ Tests failed. Keeping {TEST_DB_PATH} for inspection.")
