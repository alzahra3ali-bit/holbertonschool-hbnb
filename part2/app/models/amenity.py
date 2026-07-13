from app.models.base_model import BaseModel 

class Amenity(BaseModel):
    """
    Amenity class that represents a specific feature of a Place.
    Inherits from BaseModel.
    """

    def __init__(self, name=""):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        self._name = value
