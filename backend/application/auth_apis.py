from application.models import db
from flask import request, make_response, jsonify
from flask_security import utils, auth_token_required

def register():
    from flask import current_app
    
    body_content = request.get_json()
    
    if 'email' not in body_content or 'password' not in body_content:
        return make_response(jsonify({
            'message': 'email and password are required'
        }),400)

    email = body_content.get('email')
    password = body_content.get('password')

    # Use current_app.security.datastore instead of importing datastore
    datastore = current_app.security.datastore
    
    user = datastore.find_user(email=email)
    if user:
        return make_response(jsonify({
            'message': 'User already exists'
        }), 400)

    user_role = datastore.find_role('user')
    user = datastore.create_user(email=email, password=password, roles=[user_role])
    db.session.commit()

    return make_response(jsonify({
        'message': 'User created successfully',
        'user': {
            'email': user.email,
            'roles': [role.name for role in user.roles]
        }
    }), 201)

def login():
    from flask import current_app
    
    login_credentials = request.get_json()
    
    if 'email' not in login_credentials or 'password' not in login_credentials:
        return jsonify({
            'message': 'email and password are required'
        }), 400

    email = login_credentials.get('email')
    password = login_credentials.get('password')

    # Use current_app.security.datastore
    datastore = current_app.security.datastore
    
    user = datastore.find_user(email=email)
    if not user:
        return jsonify({
            'message': 'User does not exist'
        }), 404

    if not utils.verify_password(password, user.password):
        return jsonify({
            'message': 'Invalid password'
        }), 401

    utils.login_user(user)
    auth_token = user.get_auth_token()

    return jsonify({
        'message': 'Login successful',
        'user': {
            'email': user.email,
            'roles': [role.name for role in user.roles]
        },
        'auth_token': auth_token
    }), 200

def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authorization token required'}), 401

    utils.logout_user()
    return jsonify({
        'message': 'Logout successful'
    }), 200
