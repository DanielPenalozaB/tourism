from flask_marshmallow import Marshmallow
from app import ma
from app.models import Activity, Destination, Booking, User

# Activity Schema
class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        include_fk = True
        load_instance = True

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

# Destination Schema
class DestinationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Destination
        include_fk = True
        load_instance = True

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)

# Booking Schema
class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        include_fk = True
        load_instance = True

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = ('password_hash',)

user_schema = UserSchema()
users_schema = UserSchema(many=True)