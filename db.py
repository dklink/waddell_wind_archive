import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Import the base for creating tables

load_dotenv()

# Define the database URL
DATABASE_URL = f"postgresql://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost:5432/{os.environ["DB_NAME"]}"

# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Set up session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to initialize tables (optional)
def init_db():
    Base.metadata.create_all(bind=engine)
