from .activity_schemas import ActivitySchema
from .booking_schemas import BookingSchema
from .destination_schemas import DestinationSchema
from .role_schemas import RoleSchema
from .user_schemas import UserSchema


activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
