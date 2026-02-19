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
    grams: float = Query(None, description="Direct grams input"),
    portion: str = Query(None, description="Portion name (e.g., piece, bowl, slice)"),
    portion_count: int = Query(1, description="Number of portions"),
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

    # ----------------------------
    # Resolve final grams properly
    # ----------------------------

    final_grams = None

    # 1️⃣ If grams directly provided
    if grams is not None:
        if grams <= 0:
            return {"error": "Grams must be greater than 0"}
        final_grams = grams

    # 2️⃣ If portion provided
    elif portion:
        portion = portion.strip().lower()

        if item_type == "dish":
            from database.models import DishPortion

            portion_obj = db.query(DishPortion).filter(
                DishPortion.dish_id == item.id,
                DishPortion.portion_name.ilike(f"%{portion}%")
            ).first()


        else:
            from database.models import IngredientPortion

            portion_obj = db.query(IngredientPortion).filter(
                IngredientPortion.ingredient_id == item.id,
                IngredientPortion.portion_name.ilike(f"%{portion}%")
            ).first()


        if not portion_obj:
            return {"error": "Invalid portion selected"}

        if portion_count <= 0:
            return {"error": "Portion count must be greater than 0"}

        final_grams = portion_obj.grams * portion_count

    # 3️⃣ Default fallback
    else:
        final_grams = 100

    # ----------------------------
    # Calculate macros
    # ----------------------------

    macros = calculate_scaled_macros(item, final_grams)

    return {
        "type": item_type,
        "food_detected": item.name,
        "confidence": round(prediction["confidence"], 4),
        "grams_used": final_grams,
        "macros": macros
    }
