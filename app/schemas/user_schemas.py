from .. import ma
from ..models.user import User
from marshmallow import fields


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_login_schema = UserLoginSchema()
