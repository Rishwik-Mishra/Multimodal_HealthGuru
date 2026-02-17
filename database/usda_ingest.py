from sqlalchemy.orm import Session
from database.session import engine
from database.models import Food, Portion
from database.usda_cleaner import load_and_clean_usda
from sqlalchemy import text


BATCH_SIZE = 100


def ingest_usda():
    print("Starting USDA ingestion...")

    df = load_and_clean_usda()

    with Session(engine) as session:
        print("Clearing existing data...")
        session.execute(text("TRUNCATE TABLE portions CASCADE;"))
        session.execute(text("TRUNCATE TABLE foods CASCADE;"))
        session.commit()

        foods_to_insert = []

        print("Preparing food objects...")

        for _, row in df.iterrows():
            food = Food(
                name=row["clean_name"],
                category=row["category"],
                calories_100g=row["energy_kcal"],
                protein_100g=row["protein_g"],
                carbs_100g=row["carbs_g"],
                fat_100g=row["fat_g"],
                fiber_100g=row["fiber_g"],
                sugar_100g=row["sugar_g"],
                sat_fat_100g=row["sat_fat_g"],
                sodium_mg_100g=row["sodium_mg"]
            )
            foods_to_insert.append(food)

        print(f"Inserting {len(foods_to_insert)} foods...")

        session.bulk_save_objects(foods_to_insert)
        session.commit()

        print("Creating default 100g portions...")

        all_foods = session.query(Food).all()

        portions = [
            Portion(
                food_id=food.id,
                portion_name="100g",
                grams=100.0
            )
            for food in all_foods
        ]

        session.bulk_save_objects(portions)
        session.commit()

    print("USDA ingestion complete.")


if __name__ == "__main__":
    ingest_usda()
