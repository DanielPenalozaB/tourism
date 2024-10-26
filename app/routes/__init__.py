from flask import Blueprint

# Import routes
from . import activity_routes
from . import destination_routes
from . import booking_routes
from . import user_routes

# Initialize blueprints
activity_bp = activity_routes.bp
destination_bp = destination_routes.bp
booking_bp = booking_routes.bp
user_bp = user_routes.bp