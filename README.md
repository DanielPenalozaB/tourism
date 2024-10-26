# Tourism API Project Guide
## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup and Installation](#setup-and-installation)
3. [Project Configuration](#project-configuration)
4. [Database Schema](#database-schema)
5. [API Documentation](#api-documentation)
6. [Testing Guide](#testing-guide)
7. [Deployment Instructions](#deployment-instructions)

## Project Overview
This project is a RESTful API for a tourism application built with Flask, PostgreSQL, and Docker. The API manages tourist destinations, activities, bookings, and users, focusing on Colombian tourist sites and adventure tourism.

### Key Features
- Complete CRUD operations for destinations, activities, bookings, and users
- PostgreSQL database integration
- Docker containerization
- Data validation
- RESTful API endpoints
- Thunder Client testing collection

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Git

### Initial Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd tourism-api
```

2. Create .env file from template:
```bash
cp .env.example .env
```

3. Configure your .env file:
```.env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tourism_db
SECRET_KEY=your-secret-key-here
```

### Docker Configuration Files

1. Create `docker-compose.yml`:
```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/tourism_db
    depends_on:
      - db
    volumes:
      - .:/app
    command: flask run --host=0.0.0.0

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=tourism_db
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

2. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
```

3. Create `requirements.txt`:
```plaintext
Flask==2.0.1
Werkzeug==2.0.3
SQLAlchemy==1.4.46
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
Flask-Marshmallow==0.14.0
marshmallow-sqlalchemy==0.28.1
psycopg2-binary==2.9.5
python-dotenv==0.19.2
```

## Project Configuration

### Database Schema

The project uses four main models:

1. Destination Model (`app/models/destination.py`):
```python
from datetime import datetime
from app import db

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    activities = db.relationship('Activity', backref='destination', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

2. Activity Model (`app/models/activity.py`):
```python
from datetime import datetime
from app import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer)  # duration in minutes
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### API Routes Implementation

Example route implementation (`app/routes/activity_routes.py`):
```python
from flask import Blueprint, request, jsonify
from app import db
from app.models import Activity
from app.schemas import activity_schema, activities_schema

bp = Blueprint('activities', __name__, url_prefix='/api/activities')

@bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()

    new_activity = Activity(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        duration=data['duration'],
        destination_id=data['destination_id']
    )

    db.session.add(new_activity)
    db.session.commit()

    return activity_schema.jsonify(new_activity), 201

@bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return activities_schema.jsonify(activities)

@bp.route('/<int:id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get_or_404(id)
    return activity_schema.jsonify(activity)

@bp.route('/<int:id>', methods=['PUT'])
def update_activity(id):
    activity = Activity.query.get_or_404(id)
    data = request.get_json()

    activity.name = data.get('name', activity.name)
    activity.description = data.get('description', activity.description)
    activity.price = data.get('price', activity.price)
    activity.duration = data.get('duration', activity.duration)
    activity.destination_id = data.get('destination_id', activity.destination_id)

    db.session.commit()

    return activity_schema.jsonify(activity)

@bp.route('/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return '', 204
```

## API Documentation

### Endpoints

1. Activities Endpoints:
   - GET `/api/activities/` - List all activities
   - POST `/api/activities/` - Create a new activity
   - GET `/api/activities/<id>` - Get a specific activity

### Request/Response Examples

1. Create Activity:
```bash
POST /api/activities/
Content-Type: application/json

{
    "name": "Skying",
    "description": "Skying during winter",
    "price": 59.99,
    "duration": 60,
    "destination_id": 1
}
```

Response:
```json
{
    "created_at": "2024-10-26T04:16:50.800942",
    "description": "Skying during winter",
    "destination_id": 1,
    "duration": 60,
    "id": 1,
    "name": "Skying",
    "price": 59.99,
    "updated_at": "2024-10-26T04:16:50.800969"
}
```

## Running the Application

1. Start the containers:
```bash
docker-compose up --build
```

2. Initialize the database:
```bash
docker-compose exec web flask db upgrade
```

3. Seed the database:
```bash
python seed.py
```

## Testing with Postman

1. Import the `Postman` collection provided in the project
2. Test each endpoint:
   - Create a new activity
   - Retrieve all activities
   - Update an activity
   - Delete an activity

### Example Postman Test
```json
{
  "client": "Thunder Client",
  "collectionName": "Tourism API",
  "dateExported": "2024-10-26T10:00:00.000Z",
  "version": "1.1",
  "folders": [],
  "requests": [
    {
      "name": "Get All Activities",
      "url": "http://localhost:5000/api/activities",
      "method": "GET",
      "header": [],
      "theme": "light"
    }
  ]
}
```

## Troubleshooting

Common issues and solutions:
1. Database connection issues:
   - Check if PostgreSQL container is running
   - Verify database credentials in .env file
   - Ensure proper network configuration in docker-compose.yml

2. Migration errors:
   - Reset migrations: `docker-compose exec web flask db stamp head`
   - Create new migration: `docker-compose exec web flask db migrate`
   - Apply migration: `docker-compose exec web flask db upgrade`

