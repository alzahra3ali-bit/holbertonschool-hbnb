from app.models.base_model import BaseModel

class Place(BaseModel):
    """
    Place class that represents a property/listing.
    Inherits from BaseModel.
    """

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = []

    # --- Title Validation ---
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value

    # --- Description Validation ---
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value

    # --- Price Validation ---
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be a positive value (greater than 0)")
        self._price = float(value)

    # --- Latitude Validation ---
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    # --- Longitude Validation ---
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    # --- Owner ID Validation ---
    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str):
            raise TypeError("Owner ID must be a string")
        if not value.strip():
            raise ValueError("Owner ID cannot be empty")
        self._owner_id = value

    # --- Method to add an Amenity ---
    def add_amenity(self, amenity_id):
        """Adds an amenity ID to the place."""
        if not isinstance(amenity_id, str):
            raise TypeError("Amenity ID must be a string")
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
