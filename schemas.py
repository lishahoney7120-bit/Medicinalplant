"""
schemas.py
----------
Pydantic models — define the shape of data going in/out of the API.

UPDATED: PlantOut and PlantCreate now include habitat,
geographical_distribution, and references.
"""

import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------------------------------------------------------------------------
# Auth / Users
# ---------------------------------------------------------------------------
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime.datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------------------------------------------------------------------------
# Plants
# ---------------------------------------------------------------------------
class PlantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    class_label: str
    common_name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    medicinal_uses: Optional[str] = None
    preparation_methods: Optional[str] = None
    diseases_treated: Optional[str] = None
    active_compounds: Optional[str] = None
    side_effects: Optional[str] = None
    precautions: Optional[str] = None
    image_url: Optional[str] = None
    habitat: Optional[str] = None
    geographical_distribution: Optional[str] = None
    references: Optional[str] = None


class PlantCreate(BaseModel):
    class_label: str
    common_name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    medicinal_uses: Optional[str] = None
    preparation_methods: Optional[str] = None
    diseases_treated: Optional[str] = None
    active_compounds: Optional[str] = None
    side_effects: Optional[str] = None
    precautions: Optional[str] = None
    image_url: Optional[str] = None
    habitat: Optional[str] = None
    geographical_distribution: Optional[str] = None
    references: Optional[str] = None


# ---------------------------------------------------------------------------
# Predictions
# ---------------------------------------------------------------------------
class PredictionTopK(BaseModel):
    label: str
    confidence: float


class PredictionResult(BaseModel):
    predicted_label: str
    confidence: float
    top_k: List[PredictionTopK]
    plant: Optional[PlantOut] = None
    prediction_id: Optional[int] = None


class PredictionHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    predicted_label: str
    confidence: float
    created_at: datetime.datetime
    plant: Optional[PlantOut] = None


# ---------------------------------------------------------------------------
# Feedback / Contact
# ---------------------------------------------------------------------------
class FeedbackCreate(BaseModel):
    message: str
    rating: Optional[int] = None
    prediction_id: Optional[int] = None


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
