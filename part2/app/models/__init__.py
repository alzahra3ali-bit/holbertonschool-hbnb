#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    def __init__():
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    def save(self):
        self.updated_at = datetime.now()
    def delete(self):
        pass

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
