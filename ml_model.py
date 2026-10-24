"""
ml_model.py
-----------
Loads your trained hybrid model ONCE at server startup and exposes a
predict_from_bytes() function the API endpoint calls.
"""
 
import os
import json
import io
import numpy as np
from PIL import Image
import tensorflow as tf
 
ML_OUTPUTS_DIR = os.getenv("ML_OUTPUTS_DIR", "../outputs")  # relative to backend/ folder
MODEL_PATH = os.path.join(ML_OUTPUTS_DIR, "hybrid_plant_model.keras")
CLASS_NAMES_PATH = os.path.join(ML_OUTPUTS_DIR, "class_names.json")
IMG_SIZE = (224, 224)
TOP_K = 3
 
_model = None
_class_names = None
 
 
def load_model():
    """Called once at FastAPI startup."""
    global _model, _class_names
 
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            f"Make sure you've run train.py in the ML project first, "
            f"and that ML_OUTPUTS_DIR points to the right 'outputs' folder."
        )
    if not os.path.exists(CLASS_NAMES_PATH):
        raise FileNotFoundError(f"class_names.json not found at {CLASS_NAMES_PATH}")
 
    print(f"Loading model from {MODEL_PATH} ...")
    _model = tf.keras.models.load_model(MODEL_PATH)
 
    with open(CLASS_NAMES_PATH) as f:
        _class_names = json.load(f)
 
    print(f"Model loaded. Classes: {_class_names}")
 
 
def is_model_loaded() -> bool:
    return _model is not None
 
 
def predict_from_bytes(image_bytes: bytes):
    """
    Takes raw image bytes (from an uploaded file), returns:
        (predicted_label, confidence, top_k_list)
    where top_k_list is [{"label": ..., "confidence": ...}, ...]
    """
    if _model is None:
        raise RuntimeError("Model not loaded. Call load_model() at startup.")
 
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)  # batch dimension
 
    preds = _model.predict(img_array, verbose=0)[0]
    top_indices = preds.argsort()[-TOP_K:][::-1]
 
    top_k = [
        {"label": _class_names[i], "confidence": float(preds[i])}
        for i in top_indices
    ]
    predicted_label = top_k[0]["label"]
    confidence = top_k[0]["confidence"]
 
    return predicted_label, confidence, top_k
 