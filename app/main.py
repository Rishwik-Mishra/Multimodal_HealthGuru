import sys
import os

# Ensure project root is in path (Windows fix)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session

from database.session import SessionLocal
from services.image_service import predict_image
from services.mapping_service import map_label_to_food
from services.calorie_service import calculate_scaled_macros

app = FastAPI(title="Multimodal HealthGuru API")


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/predict")
async def predict_food(
    file: UploadFile = File(...),
    grams: float = Query(None),
    portion: str = Query(None),
    db: Session = Depends(get_db)
):
    image_bytes = await file.read()
    prediction = predict_image(image_bytes)

    item, item_type = map_label_to_food(db, prediction["label"])

    if not item:
        return {
            "error": "Food not found in database",
            "cnn_prediction": prediction
        }

    # Determine grams
    if grams:
        final_grams = grams

    elif portion and item_type == "dish":
        from database.models import DishPortion
        portion_obj = db.query(DishPortion).filter(
            DishPortion.dish_id == item.id,
            DishPortion.portion_name == portion
        ).first()

        if not portion_obj:
            return {"error": "Invalid portion selected"}

        final_grams = portion_obj.grams

    else:
        final_grams = 100  # default

    macros = calculate_scaled_macros(item, final_grams)

    return {
        "type": item_type,
        "food_detected": item.name,
        "confidence": round(prediction["confidence"], 4),
        "grams_used": final_grams,
        "macros": macros
    }

