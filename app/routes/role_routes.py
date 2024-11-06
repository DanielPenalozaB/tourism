from flask import Blueprint, request, jsonify
from app import db
from app.models import Role
from app.schemas import role_schema, roles_schema

bp = Blueprint('roles', __name__, url_prefix='/api/roles')


@bp.route('/', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return roles_schema.jsonify(roles)


@bp.route('/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get_or_404(id)
    return role_schema.jsonify(role)


@bp.route('/', methods=['POST'])
def create_role():
    data = request.get_json()

    new_role = Role(
        name=data['name'],
        description=data.get('description', '')
    )

    db.session.add(new_role)
    db.session.commit()

    return role_schema.jsonify(new_role), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()

    role.name = data.get('name', role.name)
    role.description = data.get('description', role.description)

    db.session.commit()

    return role_schema.jsonify(role)


@bp.route('/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return '', 204
