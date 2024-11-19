import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.models import Base

# Define the database URL
DATABASE_URL = os.environ["DATABASE_URL"]

# Set up the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Set up session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
