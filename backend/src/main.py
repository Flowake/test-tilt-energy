from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/entries/", response_model=schemas.Entry)
def create_user(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    print(entry)
    return crud.create_entry(db, entry=entry)
