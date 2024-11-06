from app import ma
from app.models.booking import Booking


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        include_fk = True
        load_instance = True
