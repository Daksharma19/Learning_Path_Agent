from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
    
    @staticmethod
    def create_user(username, email, password):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        user_id = db.create_user(username, email, password_hash)
        if user_id:
            user_data = db.get_user_by_id(user_id)
            return User(user_data)
        return None
    
    @staticmethod
    def get_user(username):
        """Get user by username"""
        user_data = db.get_user_by_username(username)
        if user_data:
            return User(user_data)
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user_data = db.get_user_by_id(user_id)
        if user_data:
            return User(user_data)
        return None
    
    @staticmethod
    def verify_password(username, password):
        """Verify user password"""
        user_data = db.get_user_by_username(username)
        if user_data and check_password_hash(user_data['password_hash'], password):
            return User(user_data)
        return None

