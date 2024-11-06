from app import ma
from app.models.activity import Activity


class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        include_fk = True
        load_instance = True
