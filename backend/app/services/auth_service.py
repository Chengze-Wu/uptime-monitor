import jwt
import os
from flask import request
from app.models.user import User


def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(
            token,
            os.environ.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        user = User.query.get(payload['user_id'])
        return user if user and user.is_active else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
