from datetime import datetime
from app import db

# Enrollment association table (many-to-many relationship)
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('health_program.id'), primary_key=True)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    program = db.relationship('HealthProgram', backref='enrollments')
    client = db.relationship('Client', backref='enrollments')

#Program Table
class HealthProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<HealthProgram {self.name}>'

#Client table
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.Text)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to programs
    programs = db.relationship(
        'HealthProgram', 
        secondary='enrollments',
        lazy='subquery',
        backref=db.backref('enrolled_clients', lazy=True)
    )
    
    def __repr__(self):
        return f'<Client {self.first_name} {self.last_name}>'