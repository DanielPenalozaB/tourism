from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from marshmallow import ValidationError
from .. import db
from ..models.user import User
from ..schemas.user_schemas import user_schema, user_login_schema

bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already taken"}), 400

        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": user_schema.dump(user)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = user_login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user: User = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_schema.dump(user)
    }), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": access_token}), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200


@bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    try:
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Email already exists"}), 400

        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({"error": "Username already exists"}), 400

        # Update allowed fields
        allowed_fields = ['username', 'email', 'first_name', 'last_name']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
