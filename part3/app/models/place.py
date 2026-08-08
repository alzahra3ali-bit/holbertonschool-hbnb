from app.models.basemodel import BaseModel
from app import db

class Place(BaseModel):
    _tablename_ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = []

    def validate_title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title

    def validate_description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        return description

    def validate_price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be a positive value (greater than 0)")
        return float(price)

    def validate_latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return float(latitude)

    def validate_longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return float(longitude)

    def validate_owner_id(self, owner_id):
        if not isinstance(owner_id, str):
            raise TypeError("Owner ID must be a string")
        if not owner_id.strip():
            raise ValueError("Owner ID cannot be empty")
        return owner_id
    
    def add_amenity(self, amenity_id):
        if not isinstance(amenity_id, str):
            raise TypeError("Amenity ID must be a string")
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
