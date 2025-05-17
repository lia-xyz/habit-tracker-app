from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from bson import ObjectId
from datetime import datetime
from app.extensions import mongo
from app.schemas import HabitSchema

habits = Blueprint('habits', __name__, url_prefix='/habits')

def serialize_habit(habit):
    return {
        'id': str(habit['_id']),
        'title': habit['title'],
        'frequency': habit['frequency'],
        'categories': habit['categories'],
        'created_at': habit['created_at'].isoformat()
    }

@habits.route('', methods=['POST'])
@jwt_required()
def create_habit():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        validated_data = HabitSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    habit = {
        'user_id': user_id,
        **validated_data,
        'created_at': datetime.utcnow()
    }

    result = mongo.db.habits.insert_one(habit)
    return jsonify({'message': 'Habit created', 'id': str(result.inserted_id)}), 201

@habits.route('', methods=['GET'])
@jwt_required()
def get_habits():
    user_id = get_jwt_identity()
    habits = mongo.db.habits.find({'user_id': user_id})

    return jsonify({'message': 'All habits fetched', 'data': [serialize_habit(habit) for habit in habits]}), 200

@habits.route('/<habit_id>', methods=['PUT'])
@jwt_required()
def update_habit(habit_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        object_id = ObjectId(habit_id)
    except:
        return jsonify({'error': 'Invalid habit ID'}), 400

    try:
        validated_data = HabitSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    result = mongo.db.habits.update_one(
        {'_id': object_id, 'user_id': user_id},
        {'$set': {
            'title': validated_data['title'],
            'frequency': validated_data['frequency'],
            'categories': validated_data.get('categories', [])
        }}
    )

    if result.matched_count == 0:
        return jsonify({'error': 'Habit not found'}), 404
    
    return jsonify({'message': 'Habit updated'}), 200

@habits.route('/<habit_id>', methods=['DELETE'])
@jwt_required()
def delete_habit(habit_id):
    user_id = get_jwt_identity()

    try:
        object_id = ObjectId(habit_id)
    except:
        return jsonify({'error': 'Invalid habit ID'}), 400

    result = mongo.db.habits.delete_one({
        '_id': object_id, 
        'user_id': user_id
    })

    if result.deleted_count == 0:
        return jsonify({'error': 'Habit not found'}), 404
    
    return jsonify({'message': 'Habit deleted'}), 200