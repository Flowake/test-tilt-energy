from sqlalchemy.orm import Session

import models
import schemas


def create_entry(db: Session, entry: schemas.EntryCreate) -> models.Entry:
    db_entry = models.Entry(
        email=entry.email,
        appliances=entry.appliances,
        total_consumption=entry.total_consumption,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
