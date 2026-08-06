#!/usr/bin/python3
from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        """call the attributes from parent class"""
<<<<<<< HEAD
        super.__init__()

        """Data validation"""
        if not text or len(text.strip()) == 0:
            raise ValueError('Review is required')
        if not user_id or len(user_id.strip()) == 0:
            raise ValueError('User ID is required')
        if not place_id or len(place_id.strip()) == 0:
            raise ValueError('Plase ID is required')
        if not isinstance(rating, (int, float)) or not (0 <= rating <= 5):
            raise ValueError('Rating must be a number between 0 and 5')

        """Attribute Assignment"""
        self.text = text.strip()
        self.user_id = user_id.strip()
        self.place_id = place_id.strip()
        self.rating = rating
    
    def create(self):
        """Creates and saves the review instance."""
        self.save()
        return "Review created successfully."

    def update(self, data: dict):
        """Updates the review text or rating."""
        if 'rating' in data and (not isinstance(data['rating'],(int, float)) or not 0 <= data[rating] <= 5):
            raise ValueError('Rating must be a number between 0 and 5')
        self.update(data)
    
    @classmethod
    def list(cls):
        """Class method to retrieve all reviews.""" 
        return []
        


        
=======
        super().__init__()

        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    # --- Text Validation ---
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('Review is required')
        self._text = value.strip()

    # --- Rating Validation ---
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, float)) or not (0 <= value <= 5):
            raise ValueError('Rating must be a number between 0 and 5')
        self._rating = value

    # --- User ID Validation ---
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('User ID is required')
        self._user_id = value.strip()

    # --- Place ID Validation ---
    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('Place ID is required')
        self._place_id = value.strip()

    def to_dict(self):
        """Dictionary representation of the review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
        }
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
