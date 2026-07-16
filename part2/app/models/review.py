#!/usr/bin/python3
from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        """call the attributes from parent class"""
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
        


        