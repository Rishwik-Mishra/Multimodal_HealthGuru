def calculate_scaled_macros(food, grams: float):
    factor = grams / 100.0

    return {
        "calories": round(food.calories_100g * factor, 2),
        "protein": round(food.protein_100g * factor, 2),
        "carbs": round(food.carbs_100g * factor, 2),
        "fat": round(food.fat_100g * factor, 2),
        "fiber": round(food.fiber_100g * factor, 2),
        "sugar": round(food.sugar_100g * factor, 2),
        "sat_fat": round(food.sat_fat_100g * factor, 2),
        "sodium_mg": round(food.sodium_mg_100g * factor, 2),
    }
