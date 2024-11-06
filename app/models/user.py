from flask import jsonify
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(360), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str):
        self.password = generate_password_hash(
            password, method='pbkdf2:sha1')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, email, password):
        try:
            user = cls(
                username=username,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), None
        except Exception as e:
            db.session.rollback()
            if 'users_email_key' in str(e):
                return None, "Email already exists"
            if 'users_username_key' in str(e):
                return None, "Username already exists"
            return None, str(e)

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        user: User = cls.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "Invalid credentials"
        return user.to_dict(), None

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
