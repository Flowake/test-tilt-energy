from pydantic import BaseModel


class EntryBase(BaseModel):
    email: str
    total_consumption: int
    appliances: list[str]


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int

    class Config:
        from_attributes = True
