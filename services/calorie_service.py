import pandas as pd

df = pd.read_csv("data/nutrition.csv")

def get_nutrition(food_name: str):
    food_name = food_name.lower()
    result = df[df["food"] == food_name]

    if not result.empty:
        row = result.iloc[0]
        return {
            "calories": int(row["calories"]),
            "protein": float(row["protein"]),
            "carbs": float(row["carbs"]),
            "fat": float(row["fat"])
        }
    else:
        return None
