from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )

    tasks = db.relationship(
        'Task',
        backref='owner',
        lazy=True
    )


class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.String(500)
    )

    priority = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50)
    )

    created_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # USER LINK

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )