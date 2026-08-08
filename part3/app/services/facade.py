from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    #---------- User-related methods------------------------------
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    #---------- Amenity-related methods------------------------------
    def create_amenity(self, amenity_data):
        new_amenity = Amenity(**amenity_data)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    #---------- Place-related methods------------------------------
    def create_place(self, place_data):
        place_data = dict(place_data)

        owner_id = place_data.pop('owner_id', None)
        user = self.user_repo.get(owner_id)
        if not user:
            raise KeyError('Invalid input data')

        amenity_ids = place_data.pop('amenities', None) or []
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise KeyError('Invalid input data')
            amenities.append(amenity)

        place = Place(owner_id=owner_id, **place_data)
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if not place or not amenity:
            raise KeyError('Invalid input data')
        place.add_amenity(amenity)
        self.place_repo.add(place)

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')

        place_data = dict(place_data)
        amenity_ids = place_data.pop('amenities', None)
        if amenity_ids is not None:
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError('Invalid input data')
                amenities.append(amenity)
            place.amenities = amenities

        self.place_repo.update(place_id, place_data)
        return place

    #---------- Review-related methods------------------------------
    def create_review(self, review_data):
        review_data = dict(review_data)

        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise KeyError('Invalid input data')

        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise KeyError('Invalid input data')

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError('Review not found')
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError('Review not found')
        self.review_repo.delete(review_id)
