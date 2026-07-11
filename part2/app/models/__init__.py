#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        """Assigning attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """Update the updated_at timestamp to current time"""
        self.updated_at = datetime.now()
    
    def delete(self):
        """Placeholder for deleting the object from storage"""
        pass

# Import child models to avoid circular dependencies
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
