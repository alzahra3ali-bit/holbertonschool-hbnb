from app.models.basemodel import BaseModel
from app import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='places')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = self.validate_description(description) if description else description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = self.validate_owner_id(owner_id)

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
    
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Dictionary representation of the place."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        }
