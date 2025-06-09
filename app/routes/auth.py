from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from marshmallow import ValidationError
from datetime import timedelta
from app.extensions import mongo, bcrypt
from app.schemas import UserSchema

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        validated_data = UserSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    username = validated_data['username'].strip()
    password = validated_data['password']
    email = validated_data["email"].strip()

    if mongo.db.users.find_one({'email': email}) or mongo.db.users.find_one({'username': username}):
        return jsonify({'error': 'User already registered'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_pw,
        'email': email
    })

    return jsonify({'message': 'User registered'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})

    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = create_access_token(identity=str(user['_id']), expires_delta=timedelta(days=1))

    response = make_response(jsonify({'message': 'User logged in'}))
    set_access_cookies(response, token)

    return response

@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'User logged out'})
    unset_jwt_cookies(response)

    return response