
from app import ma
from app.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        load_instance = True
