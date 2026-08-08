from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository
from sqlalchemy.exc import IntegrityError


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def create_user(self, user_data):
        try:
            user = User(**user_data)
            user.hash_password(user_data['password'])
            self.add(user)
            return user
        except IntegrityError as e:
            raise ValueError(f"Email '{user_data['email']}' is already registered") from e

    def update_user(self, user_id, user_data):
        user = self.get(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")
        
        if "password" in user_data:
            user.hash_password(user_data["password"])
            del user_data["password"]

        self.update(user_id, user_data)
        return user

    def delete_user(self, user_id):
        user = self.get(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")
        self.delete(user_id)