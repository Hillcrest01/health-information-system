from datetime import datetime
from app import db
from app.models import HealthProgram, Client, Enrollment

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
        
        # Enroll clients in programs
    tb = HealthProgram.query.filter_by(name='TB').first()
    malaria = HealthProgram.query.filter_by(name='Malaria').first()
    hiv = HealthProgram.query.filter_by(name='HIV').first()

    john = Client.query.filter_by(email='john.doe@example.com').first()
    jane = Client.query.filter_by(email='jane.smith@example.com').first()

    db.session.add(Enrollment(client_id=john.id, program_id=tb.id))
    db.session.add(Enrollment(client_id=john.id, program_id=hiv.id))
    db.session.add(Enrollment(client_id=jane.id, program_id=malaria.id))
        
    db.session.commit()
    print("Initialized database with default programs and clients")