#!/usr/bin/python3
from app.models.basemodel import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text="", rating=0):
        super().__init__()

        if not text or len(text.strip()) == 0:
            raise ValueError('Review is required')
        if not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
            raise ValueError('Rating must be a number between 1 and 5')

        self.text = text.strip()
        self.rating = rating
    
    def update(self, data: dict):
        if 'text' in data:
            self.text = data['text']
            
        if 'rating' in data:
            if not isinstance(data['rating'], (int, float)) or not (1 <= data['rating'] <= 5):
                raise ValueError('Rating must be a number between 1 and 5')
            self.rating = data['rating']