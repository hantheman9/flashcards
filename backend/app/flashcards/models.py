from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    bin = db.Column(db.Integer, default=0)
    next_review_time = db.Column(db.DateTime, default=datetime.utcnow)
    incorrect_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='flashcards')

    def __init__(self, word, definition, bin=0, next_review_time=None, incorrect_count=0, user_id=None):
        self.word = word
        self.definition = definition
        self.bin = bin
        if next_review_time is None:
            next_review_time = datetime.utcnow()
        self.next_review_time = next_review_time
        self.incorrect_count = incorrect_count
        self.user_id = user_id

    def __repr__(self):
        return f'<Flashcard {self.word}>'
    