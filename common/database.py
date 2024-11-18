import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.models import Base

# Define the database URL
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
else:
    DATABASE_URL = f"postgresql://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost:5432/{os.environ["DB_NAME"]}"

# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Set up session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
