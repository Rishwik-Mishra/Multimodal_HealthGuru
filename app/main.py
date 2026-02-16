from fastapi import FastAPI
from app.routes import router
from fastapi import UploadFile, File
import shutil
import os

from services.image_service import predict_image
from services.calorie_service import get_nutrition  # or whatever your function is named


app = FastAPI(title="HEALTH_GURU API")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "HEALTH_GURU API is running 🚀"}

@app.post("/predict-image")
async def predict_image_api(file: UploadFile = File(...)):
    
    temp_path = f"temp_{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    predicted_food, confidence = predict_image(temp_path)

    os.remove(temp_path)

    nutrition = get_nutrition(predicted_food)

    return {
        "predicted_food": predicted_food,
        "confidence": confidence,
        "nutrition": nutrition
    }

