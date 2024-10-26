class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        include_fk = True
        load_instance = True

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)