from . import activity_routes
from . import destination_routes
from . import booking_routes
from . import user_routes
from . import role_routes

# Make the blueprints available at the package level
activity_bp = activity_routes.bp
destination_bp = destination_routes.bp
booking_bp = booking_routes.bp
user_bp = user_routes.bp
role_bp = role_routes.bp
