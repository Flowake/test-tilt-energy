from pydantic import BaseModel, EmailStr


class EntryCreate(BaseModel):
    email: EmailStr
    total_consumption: float
    appliances: list[str]
    consumption_per_appliance: dict[str, float] | None = None


class Entry(BaseModel):
    id: int
    email: EmailStr
    total_consumption: float
    appliances: list[str]
    consumption_per_appliance: dict[str, float]

    class Config:
        from_attributes = True


class EntryGet(BaseModel):
    id: int
    total_consumption: float
    appliances: list[str]
    consumption_per_appliance: dict[str, float]

    class Config:
        from_attributes = True
