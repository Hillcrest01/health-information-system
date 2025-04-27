from flask import Blueprint, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models import Client


api = Blueprint('api', __name__)


#exposing the client profile here via api
@api.route('/clients/<int:client_id>')
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