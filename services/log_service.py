from sqlalchemy.orm import Session
from database.models import FoodLog


def create_food_log(
    db: Session,
    user_id: int,
    item,
    item_type: str,
    quantity_grams: float,
    macros: dict,
    portion_label: str = None
):
    log = FoodLog(
        user_id=user_id,
        food_type=item_type,
        food_id=item.id,
        food_name=item.name,
        quantity_grams=quantity_grams,
        portion_label=portion_label,
        calories=macros["calories"],
        protein=macros["protein"],
        carbs=macros["carbs"],
        fat=macros["fat"],
        fiber=macros["fiber"],
        sugar=macros["sugar"],
        sat_fat=macros["sat_fat"],
        sodium_mg=macros["sodium_mg"]
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_daily_summary(db: Session, user_id: int, date):
    from sqlalchemy import func
    from database.models import FoodLog

    result = db.query(
        func.sum(FoodLog.calories).label("calories"),
        func.sum(FoodLog.protein).label("protein"),
        func.sum(FoodLog.carbs).label("carbs"),
        func.sum(FoodLog.fat).label("fat"),
        func.sum(FoodLog.fiber).label("fiber"),
        func.sum(FoodLog.sugar).label("sugar"),
        func.sum(FoodLog.sat_fat).label("sat_fat"),
        func.sum(FoodLog.sodium_mg).label("sodium_mg"),
    ).filter(
        FoodLog.user_id == user_id,
        func.date(FoodLog.logged_at) == date
    ).first()

    return result

from datetime import datetime, timedelta
from database.models import FoodLog


def get_logs_for_date(db, user_id, query_date):
    start = datetime.combine(query_date, datetime.min.time())
    end = start + timedelta(days=1)

    logs = db.query(FoodLog).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= start,
        FoodLog.logged_at < end
    ).order_by(FoodLog.logged_at.desc()).all()

    return logs   