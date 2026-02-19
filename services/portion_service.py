from sqlalchemy import func
from database.session import SessionLocal
from database.models import DishPortion, IngredientPortion


def resolve_quantity_in_grams(
    food_id: int,
    food_type: str,
    grams=None,
    portion=None,
    portion_count: int = 1
):
    """
    Resolves final quantity in grams based on:
    - Direct grams input
    - Portion name + portion_count
    """

    if grams is not None:
        if grams <= 0:
            raise ValueError("Grams must be greater than 0")
        return grams

    if portion:
        portion = portion.strip().lower()

        db = SessionLocal()

        if food_type == "dish":
            portion_record = (
                db.query(DishPortion)
                .filter(
                    DishPortion.dish_id == food_id,
                    func.lower(DishPortion.portion_name) == portion
                )
                .first()
            )
        else:
            portion_record = (
                db.query(IngredientPortion)
                .filter(
                    IngredientPortion.ingredient_id == food_id,
                    func.lower(IngredientPortion.portion_name) == portion
                )
                .first()
            )

        db.close()

        if not portion_record:
            raise ValueError("Invalid portion size")

        if portion_count <= 0:
            raise ValueError("Portion count must be greater than 0")

        return portion_record.grams * portion_count

    raise ValueError("Either grams or portion must be provided")
