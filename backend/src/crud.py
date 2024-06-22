from sqlalchemy.orm import Session

import models
import schemas


def create_entry(db: Session, entry: schemas.EntryCreate) -> models.Entry:
    db_entry = models.Entry(
        email=entry.email,
        appliances=entry.appliances,
        total_consumption=entry.total_consumption,
        consumption_per_appliance=entry.consumption_per_appliance,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_entry(db: Session, entry_id: int) -> models.Entry | None:
    return db.query(models.Entry).filter(models.Entry.id == entry_id).first()
