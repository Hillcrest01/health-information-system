import pytest
from app import create_app, db
from app.models import Client, HealthProgram

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add test data
            program = HealthProgram(name='Test Program')
            test_client = Client(
                first_name='Test',
                last_name='User',
                email='test@example.com'
            )
            test_client.programs.append(program)
            db.session.add_all([program, test_client])
            db.session.commit()
        yield client

def test_api_unauthorized(client):
    response = client.get('/api/v1/clients/1')
    assert response.status_code == 401

def test_api_authorized(client):
    auth = ('doctor', 'health123')
    response = client.get('/api/v1/clients/1', auth=auth)
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == 'Test'
    assert len(data['programs']) == 1