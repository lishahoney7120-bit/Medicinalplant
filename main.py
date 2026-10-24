"""
main.py
-------
Main FastAPI application. Run with:
    uvicorn main:app --reload
 
Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""
 
from contextlib import asynccontextmanager
from typing import List, Optional
 
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
 
from database import Base, engine, get_db
import models
import schemas
import auth
import ml_model
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ml_model.load_model()
    yield
 
 
app = FastAPI(
    title="Medicinal Plant Recognition API",
    description="Identifies medicinal plants from leaf images using a "
                 "hybrid MobileNetV2 + ResNet50 model.",
    version="1.0.0",
    lifespan=lifespan,
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
@app.get("/")
def root():
    return {"status": "ok", "message": "Medicinal Plant Recognition API is running."}
 
 
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": ml_model.is_model_loaded(),
    }
 
 
# ===========================================================================
# AUTH
# ===========================================================================
@app.post("/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
 
    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=auth.hash_password(payload.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
 
 
@app.post("/auth/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
 
    token = auth.create_access_token({"sub": str(user.id)})
    return schemas.Token(access_token=token, user=user)
 
 
@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
 
 
# ===========================================================================
# PREDICTION
# ===========================================================================
@app.post("/predict", response_model=schemas.PredictionResult)
async def predict_plant(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")
 
    image_bytes = await file.read()
 
    try:
        predicted_label, confidence, top_k = ml_model.predict_from_bytes(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
 
    plant = db.query(models.Plant).filter(
        models.Plant.class_label == predicted_label
    ).first()
 
    prediction_id = None
    if current_user is not None:
        prediction_record = models.Prediction(
            user_id=current_user.id,
            plant_id=plant.id if plant else None,
            predicted_label=predicted_label,
            confidence=confidence,
        )
        db.add(prediction_record)
        db.commit()
        db.refresh(prediction_record)
        prediction_id = prediction_record.id
 
    return schemas.PredictionResult(
        predicted_label=predicted_label,
        confidence=confidence,
        top_k=[schemas.PredictionTopK(**t) for t in top_k],
        plant=plant,
        prediction_id=prediction_id,
    )
 
 
@app.get("/predictions/history", response_model=List[schemas.PredictionHistoryOut])
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.Prediction)
        .filter(models.Prediction.user_id == current_user.id)
        .order_by(models.Prediction.created_at.desc())
        .all()
    )
 
 
# ===========================================================================
# PLANTS
# ===========================================================================
@app.get("/plants", response_model=List[schemas.PlantOut])
def list_plants(
    search: Optional[str] = Query(None, description="Search by common or scientific name"),
    family: Optional[str] = Query(None),
    disease: Optional[str] = Query(None, description="Filter by disease treated"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Plant)
    if search:
        query = query.filter(
            or_(
                models.Plant.common_name.ilike(f"%{search}%"),
                models.Plant.scientific_name.ilike(f"%{search}%"),
            )
        )
    if family:
        query = query.filter(models.Plant.family.ilike(f"%{family}%"))
    if disease:
        query = query.filter(models.Plant.diseases_treated.ilike(f"%{disease}%"))
    return query.order_by(models.Plant.common_name).all()
 
 
@app.get("/plants/{plant_id}", response_model=schemas.PlantOut)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
 
 
@app.post("/plants", response_model=schemas.PlantOut, status_code=status.HTTP_201_CREATED)
def create_plant(
    payload: schemas.PlantCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.require_admin),
):
    existing = db.query(models.Plant).filter(
        models.Plant.class_label == payload.class_label
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="A plant with this class_label already exists")
 
    plant = models.Plant(**payload.model_dump())
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant
 
 
# ===========================================================================
# FEEDBACK / CONTACT
# ===========================================================================
@app.post("/feedback", status_code=status.HTTP_201_CREATED)
def submit_feedback(
    payload: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional),
):
    feedback = models.Feedback(
        user_id=current_user.id if current_user else None,
        prediction_id=payload.prediction_id,
        message=payload.message,
        rating=payload.rating,
    )
    db.add(feedback)
    db.commit()
    return {"status": "ok", "message": "Feedback submitted"}
 
 
@app.post("/contact", status_code=status.HTTP_201_CREATED)
def submit_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    contact = models.ContactMessage(**payload.model_dump())
    db.add(contact)
    db.commit()
    return {"status": "ok", "message": "Message received"}
 