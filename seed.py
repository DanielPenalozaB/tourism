from datetime import datetime, timedelta
from app import create_app, db
from app.models.destination import Destination
from app.models.activity import Activity
from app.models.user import User
from app.models.booking import Booking
import random

app = create_app()

def seed_database():
    """Seed the database with sample data"""

    with app.app_context():  # Create application context
        print("Starting database seeding...")

        # Clear existing data
        Booking.query.delete()
        Activity.query.delete()
        Destination.query.delete()
        User.query.delete()

        # Create destinations
        destinations = [
            Destination(
                name="Machu Picchu",
                description="Ancient Incan citadel set high in the Andes Mountains",
                country="Peru",
                city="Cusco"
            ),
            Destination(
                name="Great Barrier Reef",
                description="World's largest coral reef system",
                country="Australia",
                city="Cairns"
            ),
            Destination(
                name="Santorini",
                description="Beautiful island known for its white-washed buildings and sunsets",
                country="Greece",
                city="Thira"
            ),
            Destination(
                name="Mount Fuji",
                description="Japan's highest mountain and an iconic natural landmark",
                country="Japan",
                city="Fujinomiya"
            )
        ]

        for destination in destinations:
            db.session.add(destination)
        db.session.commit()

        # Create activities for each destination
        activities = []

        # Machu Picchu activities
        activities.extend([
            Activity(
                name="Inca Trail Trek",
                description="4-day trek through the Andes to Machu Picchu",
                price=550.00,
                duration=5760,  # 4 days in minutes
                destination_id=destinations[0].id
            ),
            Activity(
                name="Day Tour of Machu Picchu",
                description="Guided tour of the ancient citadel",
                price=150.00,
                duration=480,  # 8 hours in minutes
                destination_id=destinations[0].id
            )
        ])

        # Great Barrier Reef activities
        activities.extend([
            Activity(
                name="Scuba Diving Experience",
                description="Guided diving tour of the reef with equipment",
                price=200.00,
                duration=240,  # 4 hours in minutes
                destination_id=destinations[1].id
            ),
            Activity(
                name="Snorkeling Adventure",
                description="Snorkeling tour with marine life viewing",
                price=100.00,
                duration=180,  # 3 hours in minutes
                destination_id=destinations[1].id
            )
        ])

        # Santorini activities
        activities.extend([
            Activity(
                name="Sunset Sailing Tour",
                description="Cruise around the caldera during sunset",
                price=120.00,
                duration=240,  # 4 hours in minutes
                destination_id=destinations[2].id
            ),
            Activity(
                name="Wine Tasting Tour",
                description="Visit local wineries and taste volcanic wines",
                price=80.00,
                duration=180,  # 3 hours in minutes
                destination_id=destinations[2].id
            )
        ])

        # Mount Fuji activities
        activities.extend([
            Activity(
                name="Mount Fuji Climb",
                description="Guided climb to the summit",
                price=250.00,
                duration=720,  # 12 hours in minutes
                destination_id=destinations[3].id
            ),
            Activity(
                name="Photography Tour",
                description="Photo tour of the best Mount Fuji viewing spots",
                price=90.00,
                duration=360,  # 6 hours in minutes
                destination_id=destinations[3].id
            )
        ])

        for activity in activities:
            db.session.add(activity)
        db.session.commit()

        # Create users
        users = [
            User(
                username="john_doe",
                email="john@example.com",
                password_hash="password123",
                first_name="John",
                last_name="Doe"
            ),
            User(
                username="jane_smith",
                email="jane@example.com",
                password_hash="password123",
                first_name="Jane",
                last_name="Smith"
            ),
            User(
                username="bob_wilson",
                email="bob@example.com",
                password_hash="password123",
                first_name="Bob",
                last_name="Wilson"
            )
        ]

        for user in users:
            db.session.add(user)
        db.session.commit()

        # Create bookings
        statuses = ['pending', 'confirmed', 'cancelled']

        for _ in range(10):  # Create 10 sample bookings
            booking_date = datetime.utcnow() + timedelta(days=random.randint(1, 30))
            activity = random.choice(activities)

            booking = Booking(
                user_id=random.choice(users).id,
                activity_id=activity.id,
                booking_date=booking_date,
                number_of_people=random.randint(1, 4),
                total_price=activity.price * random.randint(1, 4),
                status=random.choice(statuses)
            )
            db.session.add(booking)

        db.session.commit()

        print("Database seeding completed!")

if __name__ == '__main__':
    seed_database()