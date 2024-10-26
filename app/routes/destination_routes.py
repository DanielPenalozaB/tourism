from flask import Blueprint, request, jsonify
from app import db
from app.models import Destination
from app.schemas import destination_schema, destinations_schema

bp = Blueprint('destinations', __name__, url_prefix='/api/destinations')

@bp.route('/', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return destinations_schema.jsonify(destinations)

@bp.route('/<int:id>', methods=['GET'])
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    return destination_schema.jsonify(destination)

@bp.route('/', methods=['POST'])
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