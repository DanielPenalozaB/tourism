from app import ma
from app.models.destination import Destination


class DestinationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Destination
        include_fk = True
        load_instance = True
