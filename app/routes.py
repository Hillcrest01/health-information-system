from flask import Blueprint, jsonify, render_template, redirect, url_for, request, make_response
from flask_httpauth import HTTPBasicAuth
from app.models import HealthProgram, Client
from app.forms import ClientForm
from app import db

main = Blueprint('main', __name__)
auth = HTTPBasicAuth()

@main.route('/')
def home():
    return render_template('clients/home.html')

@main.route('/programs')
def get_programs():
    programs = HealthProgram.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in programs])

@main.route('/clients', methods=['GET'])
def list_clients():
    clients = Client.query.all()
    return render_template('clients/list.html', clients=clients)

@main.route('/clients/register', methods=['GET', 'POST'])
def register_client():
    form = ClientForm()
    
    if form.validate_on_submit():
        client = Client(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('main.list_clients'))
    
    return render_template('clients/register.html', form=form)

@main.route('/clients/<int:client_id>')
def client_profile(client_id):
    client = Client.query.get_or_404(client_id)
    all_programs = HealthProgram.query.all()
    return render_template('clients/profile.html', 
                         client=client, 
                         programs=all_programs)

@main.route('/clients/<int:client_id>/enroll', methods=['POST'])
def enroll_client(client_id):
    client = Client.query.get_or_404(client_id)
    program_id = request.form.get('program_id')
    
    if program_id:
        program = HealthProgram.query.get(program_id)
        if program and program not in client.programs:
            client.programs.append(program)
            db.session.commit()
    
    return redirect(url_for('main.client_profile', client_id=client.id))

@main.route('/clients/<int:client_id>/unenroll/<int:program_id>')
def unenroll_client(client_id, program_id):
    client = Client.query.get_or_404(client_id)
    program = HealthProgram.query.get_or_404(program_id)
    
    if program in client.programs:
        client.programs.remove(program)
        db.session.commit()
    
    return redirect(url_for('main.client_profile', client_id=client.id))

@main.route('/clients/search')
def search_clients():
    query = request.args.get('q', '')
    if query:
        clients = Client.query.filter(
            (Client.first_name.ilike(f'%{query}%')) |
            (Client.last_name.ilike(f'%{query}%')) |
            (Client.email.ilike(f'%{query}%'))
        ).all()
    else:
        clients = []
    return render_template('clients/search.html', clients=clients, query=query)



users = {
    "doctor": "health123",  # In production, use proper password hashing
    "admin": "secure456"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@main.route('/api/clients/<int:client_id>', methods=['GET'])
@auth.login_required
def api_client_profile(client_id):
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

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)