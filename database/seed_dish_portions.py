from sqlalchemy.orm import Session
from database.session import engine
from database.models import Dish, DishPortion

DEFAULT_PORTIONS = [
    ("1 piece", 100),
    ("1 slice", 120),
    ("1 bowl", 250),
    ("1 cup", 240)
]


def seed_dish_portions():
    with Session(engine) as session:

        dishes = session.query(Dish).all()

        for dish in dishes:
            for name, grams in DEFAULT_PORTIONS:
                portion = DishPortion(
                    dish_id=dish.id,
                    portion_name=name,
                    grams=grams
                )
                session.add(portion)

        session.commit()

    print("Dish portions seeded successfully.")


if __name__ == "__main__":
    seed_dish_portions()
