from flask import Blueprint, request, jsonify
from app import db
from app.models import Booking
from app.schemas import booking_schema, bookings_schema

bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bp.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return bookings_schema.jsonify(bookings)

@bp.route('/<int:id>', methods=['GET'])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return booking_schema.jsonify(booking)