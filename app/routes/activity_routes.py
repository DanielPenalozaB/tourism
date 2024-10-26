from flask import Blueprint, request, jsonify
from app import db
from app.models import Activity
from app.schemas import activity_schema, activities_schema

bp = Blueprint('activities', __name__, url_prefix='/api/activities')

@bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()

    new_activity = Activity(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        duration=data['duration'],
        destination_id=data['destination_id']
    )

    db.session.add(new_activity)
    db.session.commit()

    return activity_schema.jsonify(new_activity), 201

@bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return activities_schema.jsonify(activities)

@bp.route('/<int:id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get_or_404(id)
    return activity_schema.jsonify(activity)

@bp.route('/<int:id>', methods=['PUT'])
def update_activity(id):
    activity = Activity.query.get_or_404(id)
    data = request.get_json()

    activity.name = data.get('name', activity.name)
    activity.description = data.get('description', activity.description)
    activity.price = data.get('price', activity.price)
    activity.duration = data.get('duration', activity.duration)
    activity.destination_id = data.get('destination_id', activity.destination_id)

    db.session.commit()

    return activity_schema.jsonify(activity)

@bp.route('/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return '', 204