from fastapi import APIRouter
from services.calorie_service import get_calories

router = APIRouter()

@router.get("/predict")
def predict_food(food_name: str):
    calories = get_calories(food_name)
    
    return {
        "food": food_name,
        "calories": calories
    }
