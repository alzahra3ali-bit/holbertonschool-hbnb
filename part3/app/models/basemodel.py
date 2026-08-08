from app import db
import uuid
from datetime import datetime, timezone

class BaseModel(db.Model):
    __abstract__ = True #we don't want to create a table for the base model.

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def is_max_length(self, name, value, max_length):
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.") 
        
    def is_between(self, name, value, min, max):
        if not min < value < max:
            raise ValueError(f"{name} must be between {min} and {max}.")