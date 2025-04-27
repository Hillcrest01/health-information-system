from datetime import datetime
from app import db
from app.models import HealthProgram, Client, Enrollment

def init_db():
    """Initialize the database"""
    db.create_all()
    
