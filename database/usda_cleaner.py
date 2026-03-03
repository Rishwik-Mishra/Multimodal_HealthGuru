import pandas as pd
import os
import re

BASE_PATH = r"data\usda"

FOOD_FILE = os.path.join(BASE_PATH, "food.csv")
FOUNDATION_FILE = os.path.join(BASE_PATH, "foundation_food.csv")
FOOD_NUTRIENT_FILE = os.path.join(BASE_PATH, "food_nutrient.csv")
NUTRIENT_FILE = os.path.join(BASE_PATH, "nutrient.csv")
CATEGORY_FILE = os.path.join(BASE_PATH, "food_category.csv")


TARGET_NUTRIENTS = {
    "Energy": "energy_kcal",
    "Protein": "protein_g",
    "Carbohydrate, by difference": "carbs_g",
    "Total lipid (fat)": "fat_g",
    "Fiber, total dietary": "fiber_g",
    "Sugars": "sugar_g",  # partial match
    "Fatty acids, total saturated": "sat_fat_g",
    "Sodium": "sodium_mg"
}


def clean_name(name):
    name = str(name).lower()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name


def load_and_clean_usda():
    print("Loading CSV files...")

    food_df = pd.read_csv(FOOD_FILE, low_memory=False)
    foundation_df = pd.read_csv(FOUNDATION_FILE, low_memory=False)
    nutrient_df = pd.read_csv(NUTRIENT_FILE, low_memory=False)
    food_nutrient_df = pd.read_csv(FOOD_NUTRIENT_FILE, low_memory=False)
    category_df = pd.read_csv(CATEGORY_FILE, low_memory=False)

    print("Filtering foundation foods...")
    foundation_ids = foundation_df["fdc_id"].unique()
    food_df = food_df[food_df["fdc_id"].isin(foundation_ids)]

    print(f"Foundation foods count: {len(food_df)}")

    # Filter nutrients only for foundation foods
    food_nutrient_df = food_nutrient_df[
        food_nutrient_df["fdc_id"].isin(foundation_ids)
    ]

    # Merge nutrient names
    food_nutrient_df = food_nutrient_df.merge(
        nutrient_df[["id", "name"]],
        left_on="nutrient_id",
        right_on="id",
        how="left"
    )

    print("Pivoting nutrients...")
    pivot_df = food_nutrient_df.pivot_table(
        index="fdc_id",
        columns="name",
        values="amount",
        aggfunc="first"
    ).reset_index()

    print("Merging food info...")
    merged_df = food_df.merge(pivot_df, on="fdc_id", how="left")

    merged_df = merged_df.merge(
        category_df[["id", "description"]],
        left_on="food_category_id",
        right_on="id",
        how="left"
    )

    merged_df.rename(columns={"description_x": "raw_name"}, inplace=True)
    merged_df.rename(columns={"description_y": "category"}, inplace=True)

    print("Mapping nutrients dynamically...")

    for key, new_col in TARGET_NUTRIENTS.items():
        matched_cols = [col for col in merged_df.columns if key in col]
        if matched_cols:
            merged_df[new_col] = merged_df[matched_cols[0]]
        else:
            merged_df[new_col] = 0

    print("Cleaning names...")
    merged_df["clean_name"] = merged_df["raw_name"].apply(clean_name)

    final_df = merged_df[
        [
            "clean_name",
            "category",
            "energy_kcal",
            "protein_g",
            "carbs_g",
            "fat_g",
            "fiber_g",
            "sugar_g",
            "sat_fat_g",
            "sodium_mg"
        ]
    ].copy()

    final_df = final_df.fillna(0)

    print(f"Final cleaned foods count: {len(final_df)}")

    return final_df


if __name__ == "__main__":
    df = load_and_clean_usda()
    print(df.head())
    print("\nUSDA cleaning complete.")
