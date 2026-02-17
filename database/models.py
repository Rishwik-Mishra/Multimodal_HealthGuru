from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)

    calories_100g = Column(Float, nullable=False)
    protein_100g = Column(Float)
    carbs_100g = Column(Float)
    fat_100g = Column(Float)
    fiber_100g = Column(Float)

    sugar_100g = Column(Float)
    sat_fat_100g = Column(Float)
    sodium_mg_100g = Column(Float)

    portions = relationship("Portion", back_populates="food", cascade="all, delete")
    logs = relationship("DailyLog", back_populates="food")

class Portion(Base):
    __tablename__ = "portions"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))
    portion_name = Column(String)
    grams = Column(Float, nullable=False)

    food = relationship("Food", back_populates="portions")


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)

    food_id = Column(Integer, ForeignKey("foods.id"))
    grams = Column(Float)

    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)

    consumed_at = Column(TIMESTAMP, server_default=func.now())

    food = relationship("Food", back_populates="logs")
