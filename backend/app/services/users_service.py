import jwt
import os
from flask import request
from app.models.user import User
from app import db


def list_users():
    return User.query.all()


def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    return user if user and user.is_active else None


def update_user(public_id, data, is_admin=False):
    user = User.query.filter_by(public_id=public_id).first()
    if data.get('firstname') is not None:
        user.firstname = data.get('firstname')
    if data.get('lastname') is not None:
        user.lastname = data.get('lastname')
    if data.get('role') is not None and is_admin:
        user.role = data.get('role')
    if data.get('is_active') is not None and is_admin:
        user.is_active = data.get('is_active')
    db.session.commit()
    return user
