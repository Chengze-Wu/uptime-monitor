import jwt
import os
from flask import request
from app.models.user import User


def list_users():
    return User.query.all()


def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    return user if user and user.is_active else None
