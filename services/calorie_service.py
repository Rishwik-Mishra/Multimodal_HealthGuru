import pandas as pd

# Load CSV once
df = pd.read_csv("data/nutrition.csv")

def get_calories(food_name: str):
    food_name = food_name.lower()
    
    result = df[df["food"] == food_name]
    
    if not result.empty:
        return int(result["calories"].values[0])
    else:
        return "Food not found in database"
