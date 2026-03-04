from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.middleware.auth_middleware import require_admin, require_auth
from app.services import users_service, auth_service

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
@require_admin
def list_users():
    users = users_service.list_users()
    return jsonify({'users': [u.to_dict() for u in users]}), 200


@users_bp.route('/<public_id>', methods=['GET'])
@require_auth
def get_user(public_id):
    current = auth_service.get_current_user()
    user = users_service.get_user(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if current.public_id == user.public_id or current.role == 'admin':
        return jsonify({'user': user.to_dict()}), 200

    return jsonify({'error': 'User not found'}), 404


@users_bp.route('/<public_id>', methods=['PUT'])
@require_auth
def update_user(public_id):
    data = request.get_json()
    current = auth_service.get_current_user()
    user = users_service.get_user(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if current.role == 'admin':
        updated_user = users_service.update_user(public_id, data, is_admin=True)
    elif current.public_id == user.public_id:
        updated_user = users_service.update_user(public_id, data, data, is_admin=False)
    else:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': updated_user.to_dict()}), 200
