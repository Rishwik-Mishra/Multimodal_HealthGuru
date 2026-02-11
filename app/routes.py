from fastapi import APIRouter
from services.calorie_service import get_nutrition
from services.nlp_service import extract_food_items

router = APIRouter()

@router.get("/predict")
def predict_food(query: str):
    items = extract_food_items(query)

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    detailed_breakdown = []

    for item in items:
        nutrition = get_nutrition(item["food"])

        if nutrition:
            multiplier = item["quantity"]

            total_calories += nutrition["calories"] * multiplier
            total_protein += nutrition["protein"] * multiplier
            total_carbs += nutrition["carbs"] * multiplier
            total_fat += nutrition["fat"] * multiplier

            detailed_breakdown.append({
                "food": item["food"],
                "quantity": multiplier,
                "calories_per_unit": nutrition["calories"],
                "protein_per_unit": nutrition["protein"],
                "carbs_per_unit": nutrition["carbs"],
                "fat_per_unit": nutrition["fat"]
            })

    return {
        "items": detailed_breakdown,
        "totals": {
            "calories": round(total_calories, 2),
            "protein": round(total_protein, 2),
            "carbs": round(total_carbs, 2),
            "fat": round(total_fat, 2)
        }
    }
