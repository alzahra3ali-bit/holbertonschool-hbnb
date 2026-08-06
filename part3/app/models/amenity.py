from app.models.basemodel import BaseModel

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
<<<<<<< HEAD
=======

    def to_dict(self):
        """Dictionary representation of the amenity."""
        return {
            'id': self.id,
            'name': self.name,
        }
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
