from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="HEALTH_GURU API")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "HEALTH_GURU API is running 🚀"}
