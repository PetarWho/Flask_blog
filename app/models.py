from datetime import datetime, timezone
from app import db
import uuid


class BaseEntityModel(db.Model):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class

    def save(self):
        """Save the current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database."""
        db.session.delete(self)
        db.session.commit()


class User(BaseEntityModel):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(BaseEntityModel):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Markdown content
    cover_image = db.Column(db.String(200), nullable=True)
    views_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'
