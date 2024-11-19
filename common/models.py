from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    archived_at = Column(TIMESTAMP(timezone=True), index=True, nullable=False)
    filename = Column(String, nullable=False)
