from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.schemas import user_schema, users_schema
from flask_jwt_extended import jwt_required

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(
        new_user
    ), 201
