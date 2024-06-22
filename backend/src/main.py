from fastapi import Depends, FastAPI
from fastapi.responses import Response
from sqlalchemy.orm import Session

import models
import schemas
import crud
import logic
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/entries", response_model=schemas.EntryGet)
def create_user(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    if len(entry.appliances) == 0:
        return Response(status_code=400, content="Appliances list cannot be empty")
    # We receive kWh and convert it to Wh
    if (
        output := logic.appliances_to_energy(
            entry.appliances, entry.total_consumption * 1000
        )
    ) is None:
        return Response(
            status_code=400,
            content="Impossible to compute the energy consumption per appliance",
        )
    entry.consumption_per_appliance = output
    return crud.create_entry(db, entry=entry)


@app.get("/entries/{entry_id}", response_model=schemas.EntryGet)
def read_item(entry_id: int, db: Session = Depends(get_db)):
    return crud.get_entry(db, entry_id)
