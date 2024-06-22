from sqlalchemy import ARRAY, Column, Integer, String

from database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    total_consumption = Column(Integer)
    appliances = Column(ARRAY(String))
