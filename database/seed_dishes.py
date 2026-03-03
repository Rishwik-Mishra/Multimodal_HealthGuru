from sqlalchemy.orm import Session
from database.session import engine
from database.models import Dish
from database.curated_dish_data import CURATED_DISH_NUTRITION


def seed_dishes():
    with Session(engine) as session:

        session.query(Dish).delete()

        seeded_count = 0

        for name, nutrition in CURATED_DISH_NUTRITION.items():

            dish = Dish(
                name=name,
                calories_100g=nutrition["calories"],
                protein_100g=nutrition["protein"],
                carbs_100g=nutrition["carbs"],
                fat_100g=nutrition["fat"],
                fiber_100g=nutrition["fiber"],
                sugar_100g=nutrition["sugar"],
                sat_fat_100g=nutrition["sat_fat"],
                sodium_mg_100g=nutrition["sodium"]
            )

            session.add(dish)
            seeded_count += 1

        session.commit()

    print(f"Seeded {seeded_count} dishes from curated dataset.")


if __name__ == "__main__":
    seed_dishes()