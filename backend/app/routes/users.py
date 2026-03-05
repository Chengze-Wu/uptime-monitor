from flask import Blueprint, request, jsonify, abort
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
    is_admin = current.role == 'admin'
    is_self = current.public_id == public_id

    if not is_admin and not is_self:
        return jsonify({'error': 'User not found'}), 404
    user = users_service.get_user_regardless_status(public_id) if is_admin else users_service.get_user(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    updated_user = users_service.update_user(user, data, is_admin=is_admin)
    return jsonify({'user': updated_user.to_dict()}), 200


@users_bp.route('/<public_id>', methods=['DELETE'])
@require_auth
def disable_user(public_id):
    current = auth_service.get_current_user()
    is_admin = current.role == 'admin'
    is_self = current.public_id == public_id

    if not is_admin and not is_self:
        return jsonify({'error': 'User not found'}), 404

    user = users_service.get_user(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'admin' and not is_self:
        return jsonify({'error': 'User not found'}), 404

    users_service.disable_user(user)
    return '', 204


@users_bp.route('/<public_id>/purge', methods=['DELETE'])
@require_admin
def delete_user(public_id):
    current = auth_service.get_current_user()
    is_self = current.public_id == public_id

    if is_self:
        return jsonify({'error': 'Forbidden'}), 403

    user = users_service.get_user(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.role == 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    users_service.delete_user(user)
    return '', 204


@users_bp.route('/<public_id>/enable', methods=['PUT'])
@require_admin
def enable_user(public_id):
    user = users_service.get_user_regardless_status(public_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    users_service.enable_user(user)
    jsonify({'user': user.to_dict()}), 200
