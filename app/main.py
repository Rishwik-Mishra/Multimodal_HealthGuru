import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Depends, Query, Body
from sqlalchemy.orm import Session
from datetime import date

from database.session import SessionLocal
from database.models import User, Dish, DishPortion, IngredientPortion
from services.image_service import predict_image
from services.mapping_service import map_label_to_food
from services.calorie_service import calculate_scaled_macros
from services.log_service import create_food_log, get_daily_summary, get_logs_for_date

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Multimodal HealthGuru API")


# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Database Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Temporary Test User
# ----------------------------
def ensure_test_user(db):
    user = db.query(User).filter(User.email == "test@healthguru.ai").first()
    if not user:
        user = User(email="test@healthguru.ai")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# ----------------------------
# Predict Endpoint
# ----------------------------
@app.post("/predict")
async def predict_food(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await file.read()
    prediction = predict_image(image_bytes)

    item, item_type = map_label_to_food(db, prediction["label"])

    if not item:
        return {"error": "Food not found in database"}

    final_grams = 100
    macros = calculate_scaled_macros(item, final_grams)

    return {
        "dish_id": item.id,  # ✅ IMPORTANT
        "type": item_type,
        "food_detected": item.name,
        "confidence": round(prediction["confidence"], 4),
        "grams_used": final_grams,
        "macros": macros
    }


# ----------------------------
# Log Food Endpoint (JSON-based)
# ----------------------------
@app.post("/log-food")
def log_food(
    dish_id: int = Body(...),
    portion_count: float = Body(...),
    grams: float = Body(...),
    db: Session = Depends(get_db)
):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()

    if not dish:
        return {"error": "Dish not found"}

    if grams <= 0:
        return {"error": "Grams must be greater than 0"}

    macros = calculate_scaled_macros(dish, grams)

    user = ensure_test_user(db)

    log = create_food_log(
        db=db,
        user_id=user.id,
        item=dish,
        item_type="dish",
        quantity_grams=grams,
        macros=macros,
        portion_label=f"{portion_count}x"
    )

    return {
        "message": "Food logged successfully",
        "log_id": log.id,
        "grams": grams,
        "macros": macros
    }


# ----------------------------
# Daily Summary
# ----------------------------
@app.get("/daily-summary")
def daily_summary(
    query_date: date,
    db: Session = Depends(get_db)
):
    user = ensure_test_user(db)
    summary = get_daily_summary(db, user.id, query_date)

    if summary:
        summary_dict = {
            "calories": float(summary.calories or 0),
            "protein": float(summary.protein or 0),
            "carbs": float(summary.carbs or 0),
            "fat": float(summary.fat or 0),
            "fiber": float(summary.fiber or 0),
            "sugar": float(summary.sugar or 0),
            "sat_fat": float(summary.sat_fat or 0),
            "sodium_mg": float(summary.sodium_mg or 0),
        }
    else:
        summary_dict = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "sugar": 0,
            "sat_fat": 0,
            "sodium_mg": 0,
        }

    return {
        "date": query_date,
        "summary": summary_dict
    }


# ----------------------------
# Get Logs
# ----------------------------
@app.get("/logs")
def get_logs(
    query_date: date,
    db: Session = Depends(get_db)
):
    user = ensure_test_user(db)
    logs = get_logs_for_date(db, user.id, query_date)

    formatted_logs = []

    for log in logs:
        formatted_logs.append({
            "log_id": log.id,
            "food_name": log.food_name,
            "food_type": log.food_type,
            "grams": log.quantity_grams,
            "portion": log.portion_label,
            "calories": log.calories,
            "protein": log.protein,
            "carbs": log.carbs,
            "fat": log.fat,
            "fiber": log.fiber,
            "sugar": log.sugar,
            "sat_fat": log.sat_fat,
            "sodium_mg": log.sodium_mg,
            "logged_at": log.logged_at
        })

    return {
        "date": query_date,
        "total_items": len(formatted_logs),
        "logs": formatted_logs
    }

@app.get("/search-dish")
def search_dish(query: str, db: Session = Depends(get_db)):
    dishes = (
        db.query(Dish)
        .filter(Dish.name.ilike(f"%{query}%"))
        .limit(10)
        .all()
    )

    return dishes