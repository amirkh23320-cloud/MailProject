from datetime import datetime

from .database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    sent_letters = db.relationship(
        "Letter",
        foreign_keys="Letter.sender_id",
        back_populates="sender",
        lazy=True
    )

    received_letters = db.relationship(
        "Letter",
        foreign_keys="Letter.receiver_id",
        back_populates="receiver",
        lazy=True
    )


class Letter(db.Model):
    __tablename__ = "letters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    subject = db.Column(
        db.String(200),
        nullable=False
    )

    body = db.Column(
        db.Text,
        nullable=False
    )

    attachment = db.Column(
        db.String(255),
        nullable=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_letters"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_letters"
    )