from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = ('password_hash',)  # Don't expose password hash

user_schema = UserSchema()
users_schema = UserSchema(many=True)