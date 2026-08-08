from app.models.basemodel import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user = db.relationship('User', backref='reviews')
    place = db.relationship('Place', backref='reviews')

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()

        if not text or len(text.strip()) == 0:
            raise ValueError('Review is required')
        if not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
            raise ValueError('Rating must be a number between 1 and 5')

        self.text = text.strip()
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def update(self, data: dict):
        if 'text' in data:
            self.text = data['text']

        if 'rating' in data:
            if not isinstance(data['rating'], (int, float)) or not (1 <= data['rating'] <= 5):
                raise ValueError('Rating must be a number between 1 and 5')
            self.rating = data['rating']

        db.session.commit()

    def to_dict(self):
        """Dictionary representation of the review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        }