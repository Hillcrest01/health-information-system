from datetime import datetime
from app import db
from app.models import HealthProgram, Client

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
        
        # Add sample clients
        clients = [
            Client(
                first_name='John',
                last_name='Doe',
                date_of_birth=datetime(1985, 5, 15),
                gender='Male',
                contact_number='+1234567890',
                email='john.doe@example.com'
            ),
            Client(
                first_name='Jane',
                last_name='Smith',
                date_of_birth=datetime(1990, 8, 22),
                gender='Female',
                contact_number='+0987654321',
                email='jane.smith@example.com'
            )
        ]
        db.session.add_all(clients)
        
        # Enroll clients in programs
        clients[0].programs.append(programs[0])  # John in TB
        clients[0].programs.append(programs[2])  # John in HIV
        clients[1].programs.append(programs[1])  # Jane in Malaria
        
        db.session.commit()
        print("Initialized database with default programs and clients")