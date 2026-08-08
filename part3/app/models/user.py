from app import db, bcrypt
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, plain_password):
        """Hashes the password and stores it."""
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, plain_password):
        """Verifies a plain password against the hashed one."""
        return bcrypt.check_password_hash(self.password, plain_password)
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email or '.' not in email.split('@', 1)[1]:
            raise ValueError('Invalid email address')
        return email.strip()

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError(f'{key.replace("_", " ").capitalize()} is required')
        return name.strip()
    