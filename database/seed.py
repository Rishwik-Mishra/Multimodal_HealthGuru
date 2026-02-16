from database.session import SessionLocal
from database.models import Food


def seed_data():
    db = SessionLocal()

    foods = [
        Food(name="pizza", category="fast_food", calories_100g=266, protein_100g=11, carbs_100g=33, fat_100g=10),
        Food(name="banana", category="fruit", calories_100g=89, protein_100g=1.1, carbs_100g=23, fat_100g=0.3),
        Food(name="rice", category="grain", calories_100g=130, protein_100g=2.7, carbs_100g=28, fat_100g=0.3),
    ]

    for food in foods:
        existing = db.query(Food).filter(Food.name == food.name).first()
        if not existing:
            db.add(food)

    db.commit()
    db.close()
    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed_data()
