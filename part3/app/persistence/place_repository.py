from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_places_by_user(self, user_id):
        return self.model.query.filter_by(owner_id=user_id).all()

    def get_places_by_amenity(self, amenity_id):
        return self.model.query.filter(self.model.amenities.any(id=amenity_id)).all()

    def get_places_by_price_range(self, min_price, max_price):
        return self.model.query.filter(self.model.price >= min_price, self.model.price <= max_price).all()

    def add_amenity_to_place(self, place_id, amenity):
        place = self.get(place_id)
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found")

        if amenity not in place.amenities:
            place.amenities.append(amenity)
            db.session.commit()

    def remove_amenity_from_place(self, place_id, amenity):
        place = self.get(place_id)
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found")

        if amenity in place.amenities:
            place.amenities.remove(amenity)
            db.session.commit()