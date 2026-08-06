from app import bcrypt
from app.models import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):

        """Call the attributes from parent class"""
        super().__init__()

        """Data validation"""
        if not first_name or len(first_name.strip()) == 0:
            raise ValueError('First name is required')
        if not last_name or len(last_name.strip()) == 0:
            raise ValueError('Last name is required')
        if not email or '@' not in email or '.' not in email.split('@', 1)[1]:
            raise ValueError('Invalid email address')
        if not password or len(password.strip()) == 0:
            raise ValueError('Password is required')

        """Attribute Assignment,
        .strip() removes accidental leading/trailing spaces from inputs
        """
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
        self.hash_password(password.strip())
        self.places = []
        self.reviews = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def register(self):
        """Registers the user in the system."""
        self.save()
        return f"User {self.email} registered successfully."
       
    def update_profile(self, data : dict):
       """Updates the user's profile with a given dictionary of new data."""
       self.update(data)

    def add_place(self, place):
        """Adds a place to the user's owned places."""
        self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's reviews."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Removes a review from the user's reviews."""
        if review in self.reviews:
            self.reviews.remove(review)

    @classmethod
    def list(cls):
        """Class method to retrieve all users."""
        return []
