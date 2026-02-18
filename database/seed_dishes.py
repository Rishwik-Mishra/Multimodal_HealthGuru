import json
from sqlalchemy.orm import Session
from database.session import engine
from database.models import Dish
from database.curated_dish_data import CURATED_DISH_NUTRITION

CLASS_NAMES_PATH = "models/cnn/class_names.json"

# Fallback average values
DEFAULT_VALUES = {
    "calories": 200,
    "protein": 8,
    "carbs": 25,
    "fat": 8,
    "fiber": 2,
    "sugar": 5,
    "sat_fat": 3,
    "sodium": 300
}


def seed_dishes_from_cnn():
    with open(CLASS_NAMES_PATH, "r") as f:
        class_names = json.load(f)

    with Session(engine) as session:

        session.query(Dish).delete()

        for name in class_names:

            nutrition = CURATED_DISH_NUTRITION.get(name, DEFAULT_VALUES)

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

        session.commit()

    print(f"Seeded {len(class_names)} dishes with curated + default nutrition.")


if __name__ == "__main__":
    seed_dishes_from_cnn()
