from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from bson import ObjectId
from app.extensions import mongo
from app.schemas import LogSchema

logs = Blueprint('logs', __name__)

def serialize_log(log):
    return {
        'id': str(log['_id']),
        'habit_id': log['habit_id'],
        'date': log['date'].isoformat()
    }

@logs.route('/habits/<habit_id>/logs', methods=['POST'])
@jwt_required()
def create_log(habit_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        validated_data = LogSchema().load(data)
        from datetime import datetime, time
        validated_data['date'] = datetime.combine(validated_data['date'], time.min)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    existing_log = mongo.db.logs.find_one({
        'user_id': user_id,
        'habit_id': habit_id,
        **validated_data
    })

    if existing_log:
        return jsonify({'error': 'Log already exists'}), 400

    log = {
        'user_id': user_id,
        'habit_id': habit_id,
        **validated_data
    }

    result = mongo.db.logs.insert_one(log)

    return jsonify({'message': 'Log created', 'id': str(result.inserted_id)}), 201

@logs.route('/logs/<log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    user_id = get_jwt_identity()

    try:
        object_id = ObjectId(log_id)
    except:
        return jsonify({'error': 'Invalid log ID'}), 400
    
    result = mongo.db.logs.delete_one({
        '_id': object_id, 
        'user_id': user_id
    })

    if result.deleted_count == 0:
        return jsonify({'error': 'Log not found'}), 404
    
    return jsonify({'message': 'Log deleted'}), 200

@logs.route('/habits/<habit_id>/logs', methods=['GET'])
@jwt_required()
def get_logs(habit_id):
    user_id = get_jwt_identity()
    logs = mongo.db.logs.find({'user_id': user_id, 'habit_id': habit_id})

    return jsonify({'message': 'All logs fetched', 'data': [serialize_log(log) for log in logs]}), 200