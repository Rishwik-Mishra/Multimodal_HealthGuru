from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import Optional

from services.image_service import predict_image
from services.mapping_service import resolve_food_mapping
from services.portion_service import resolve_quantity_in_grams
from services.calorie_service import calculate_scaled_macros

router = APIRouter()


@router.post("/predict")
async def predict_food(
    file: UploadFile = File(...),
    grams: Optional[float] = Query(None, description="Direct quantity in grams"),
    portion: Optional[str] = Query(None, description="Portion name (e.g., piece, bowl, slice)"),
    portion_count: Optional[int] = Query(1, description="Number of portions")
):
    try:
        # 1️⃣ CNN Prediction
        label, confidence = predict_image(file)

        # 2️⃣ Map label → Dish or Ingredient
        food_record, food_type = resolve_food_mapping(label)

        if not food_record:
            raise HTTPException(status_code=404, detail="Food not found in database")

        # 3️⃣ Resolve final grams
        quantity_grams = resolve_quantity_in_grams(
            food_id=food_record.id,
            food_type=food_type,
            grams=grams,
            portion=portion,
            portion_count=portion_count
        )

        # 4️⃣ Calculate scaled macros
        macros = calculate_scaled_macros(
            food_record=food_record,
            quantity_grams=quantity_grams
        )

        return {
            "label": label,
            "confidence": confidence,
            "food_type": food_type,
            "quantity_grams": quantity_grams,
            "macros": macros
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
