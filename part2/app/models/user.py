from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password_hash, is_admin=False):
        
        """Call the attributes from parent class"""
        super().__init__()

        """Data validation"""
        if not first_name or len(first_name.strip()) == 0:
            raise ValueError('First name is required')
        if not last_name or len(last_name.strip()) == 0:
            raise ValueError('Last name is required')
        if not email or '@' not in email:
            raise ValueError('Invalid email address')

        """Attribute Assignment,
        .strip() removes accidental leading/trailing spaces from inputs
        """
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
        self.password = password_hash.strip()

    def register(self):
        """Registers the user in the system."""
        self.save()
        return f"User {self.email} registered successfully."
       
    def update_profile(self, data : dict):
       """Updates the user's profile with a given dictionary of new data."""
       self.update(data)
           
    
       
    @classmethod
    def list(cls):
        """Class method to retrieve all users."""
        return []
