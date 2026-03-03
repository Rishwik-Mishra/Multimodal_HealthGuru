from sqlalchemy.orm import Session
from database.models import Food, Dish


def normalize_label(label: str):
    return label.lower().replace(" ", "_")


def map_label_to_food(db: Session, label: str):
    label = normalize_label(label)

    # Direct dish lookup (100% coverage now)
    dish = db.query(Dish).filter(Dish.name == label).first()
    if dish:
        return dish, "dish"

    # Fallback to ingredient DB
    food = db.query(Food).filter(Food.name.ilike(f"%{label}%")).first()
    if food:
        return food, "ingredient"

    return None, None
