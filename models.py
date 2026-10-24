"""
models.py
---------
SQLAlchemy ORM models. Covers: Users (with role field for admin/registered
user), Plants (medicinal plant info), Predictions (history), Feedback,
and ContactMessages.

UPDATED: Plant now includes habitat, geographical_distribution, and
references — needed for the "Other Information" frontend page.
"""

import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # "user" or "admin"
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    predictions = relationship("Prediction", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    class_label = Column(String(100), unique=True, index=True, nullable=False)  # must match ML model's class name
    common_name = Column(String(150), nullable=False)
    scientific_name = Column(String(150))
    family = Column(String(100))
    medicinal_uses = Column(Text)
    preparation_methods = Column(Text)
    diseases_treated = Column(Text)
    active_compounds = Column(Text)
    side_effects = Column(Text)
    precautions = Column(Text)
    image_url = Column(String(255), nullable=True)

    # New fields for the "Other Information" page
    habitat = Column(Text, nullable=True)
    geographical_distribution = Column(Text, nullable=True)
    references = Column(Text, nullable=True)

    predictions = relationship("Prediction", back_populates="plant")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # null = guest prediction
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=True)
    predicted_label = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="predictions")
    plant = relationship("Plant", back_populates="predictions")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="favorites")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
