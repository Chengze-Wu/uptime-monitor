import jwt
import os
from flask import request
from app.models.user import User
from app import db
from werkzeug.exceptions import BadRequestKeyError


def list_users():
    return User.query.all()


def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    return user if user and user.is_active else None


def get_user_regardless_status(public_id):
    return User.query.filter_by(public_id=public_id).first()


def update_user(user, data, is_admin=False):
    if data.get('firstname') is not None:
        user.firstname = data.get('firstname')
    if data.get('lastname') is not None:
        user.lastname = data.get('lastname')
    if data.get('role') is not None and is_admin:
        user.role = data.get('role')
    db.session.commit()
    return user


def disable_user(user):
    user.is_active = False
    db.session.commit()


def delete_user(user):
    db.session.delete(user)
    db.session.commit()


def enable_user(user):
    user.is_active = True
    db.session.commit()
