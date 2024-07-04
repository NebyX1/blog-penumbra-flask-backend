from datetime import datetime, timezone
from flask_login import UserMixin
from .db import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def check_password(self, password_attempt):
        return self.password == password_attempt

    def __repr__(self):
        return "<Admin %r>" % self.id

    def serialize(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(250))
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "date": self.date.isoformat(),
            "category": self.category,
            "slug": self.slug,
            "image": self.image,
            "title": self.title,
            "content": self.content
        }
