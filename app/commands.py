from app import db
from app.models import HealthProgram

def init_db():
    """Initialize the database"""
    db.create_all()
    
    # Add some default programs if none exist
    if not HealthProgram.query.first():
        programs = [
            HealthProgram(name='TB', description='Tuberculosis program'),
            HealthProgram(name='Malaria', description='Malaria prevention'),
            HealthProgram(name='HIV', description='HIV/AIDS treatment')
        ]
        db.session.add_all(programs)
        db.session.commit()
        print("Initialized database with default programs")