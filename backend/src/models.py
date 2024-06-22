from sqlalchemy import ARRAY, Column, Integer, String, Float

from database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    total_consumption = Column(Float)
    appliances = Column(ARRAY(String))
