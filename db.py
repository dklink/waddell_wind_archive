import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Import the base for creating tables

# Define the database URL
DATABASE_URL = f"postgresql://{os.environ["db_username"]}:{os.environ["db_password"]}@localhost:5432/waddell_wind_archive"

# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Set up session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to initialize tables (optional)
def init_db():
    Base.metadata.create_all(bind=engine)
