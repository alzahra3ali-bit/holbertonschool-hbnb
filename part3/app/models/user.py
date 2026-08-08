from app import db, bcrypt
from app.models.basemodel import BaseModel

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