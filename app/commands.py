#Initialize the database
from app import db

def init_db():
    """Initialize the database"""
    db.create_all()
    
