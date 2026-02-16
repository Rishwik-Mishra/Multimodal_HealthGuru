from database.session import SessionLocal
from database.models import Food


def calculate_macros(food_name: str, grams: float):
    db = SessionLocal()

    food = db.query(Food).filter(Food.name == food_name.lower()).first()

    if not food:
        db.close()
        return {"error": "Food not found in database"}

    factor = grams / 100.0

    result = {
        "calories": food.calories_100g * factor,
        "protein": (food.protein_100g or 0) * factor,
        "carbs": (food.carbs_100g or 0) * factor,
        "fat": (food.fat_100g or 0) * factor,
    }

    db.close()
    return result
