from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import Config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import models and schemas
        from .models import Activity, Destination, Booking, User
        from .schemas import activity_schema, activities_schema
        from .routes import activity_routes, destination_routes, booking_routes, user_routes

        # Register blueprints
        app.register_blueprint(activity_routes.bp)
        app.register_blueprint(destination_routes.bp)
        app.register_blueprint(booking_routes.bp)
        app.register_blueprint(user_routes.bp)

        # Create all database tables
        db.create_all()

    return app