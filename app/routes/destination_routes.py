from flask import Blueprint, request, jsonify
from app import db
from app.models import Destination
from app.schemas import destination_schema, destinations_schema
from flask_jwt_extended import jwt_required

bp = Blueprint('destinations', __name__, url_prefix='/api/destinations')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_destinations():
    destinations = Destination.query.all()
    return destinations_schema.jsonify(destinations)


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    return destination_schema.jsonify(destination)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_destination():
    data = request.get_json()
    new_destination = Destination(
        name=data['name'],
        description=data.get('description', ''),
        country=data['country'],
        city=data['city']
    )
    db.session.add(new_destination)
    db.session.commit()
    return destination_schema.jsonify(new_destination), 201
