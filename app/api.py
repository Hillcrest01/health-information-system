from flask import Blueprint, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models import Client
from app import auth

api = Blueprint('api', __name__)

@api.route('/clients/<int:client_id>')
@auth.login_required
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email,
        'programs': [{
            'id': p.id,
            'name': p.name,
            'enrollment_date': client.enrollments.filter_by(program_id=p.id).first().enrollment_date.isoformat()
        } for p in client.programs]
    })