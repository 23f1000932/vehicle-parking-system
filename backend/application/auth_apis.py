from application.models import db, User
from flask import request, make_response, jsonify
from flask_security import utils
from flask import current_app

def register():
    body_content = request.get_json()
    
    required_fields = ['email', 'password', 'name', 'address', 'pin']
    # Check if all required fields are present
    if not all(field in body_content for field in required_fields):
        return make_response(jsonify({
            'message': f'Missing required fields. Required: {", ".join(required_fields)}'
        }), 400)

    datastore = current_app.security.datastore
    
    # Check if user already exists
    if datastore.find_user(email=body_content.get('email')):
        return make_response(jsonify({'message': 'User already exists'}), 400)

    user_role = datastore.find_role('user')
    user = datastore.create_user(
        email=body_content.get('email'), 
        password=body_content.get('password'), 
        name=body_content.get('name'),
        address=body_content.get('address'),
        pin=body_content.get('pin'),
        roles=[user_role]
    )
    db.session.commit()

    return make_response(jsonify({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'address': user.address,
            'pin': user.pin,
            'roles': [role.name for role in user.roles]
        }
    }), 201)

def login():
    login_credentials = request.get_json()
    
    # Checking email and password are provided
    if 'email' not in login_credentials or 'password' not in login_credentials:
        return jsonify({'message': 'email and password are required'}), 400

    email = login_credentials.get('email')
    password = login_credentials.get('password')

    datastore = current_app.security.datastore
    user = datastore.find_user(email=email)

    # Check if user exists
    if not user:
        return jsonify({'message': 'User does not exist'}), 404
    
    # Verify password
    if not utils.verify_password(password, user.password):
        return jsonify({'message': 'Invalid password'}), 401

    # Generate auth token    
    auth_token = user.get_auth_token()

    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'address': user.address,
            'pin': user.pin,
            'roles': [role.name for role in user.roles]
        },
        'auth_token': auth_token
    }), 200

def logout():
    return jsonify({'message': 'Logout successful'}), 200
