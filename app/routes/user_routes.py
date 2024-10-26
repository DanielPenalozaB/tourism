from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.schemas import user_schema, users_schema

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(
        new_user
    ), 201