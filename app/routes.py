from flask import Blueprint, jsonify
from app.models import HealthProgram

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({'message': 'Health Info System API'})

@main.route('/programs')
def get_programs():
    programs = HealthProgram.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in programs])