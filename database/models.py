from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime,TIMESTAMP
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

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    calories_100g = Column(Float, nullable=False)
    protein_100g = Column(Float)
    carbs_100g = Column(Float)
    fat_100g = Column(Float)
    fiber_100g = Column(Float)

    sugar_100g = Column(Float)
    sat_fat_100g = Column(Float)
    sodium_mg_100g = Column(Float)

class DishPortion(Base):
    __tablename__ = "dish_portions"

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    portion_name = Column(String)
    grams = Column(Float)

class IngredientPortion(Base):
    __tablename__ = "ingredient_portions"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("foods.id"))
    portion_name = Column(String)
    grams = Column(Float)


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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    logs = relationship("FoodLog", back_populates="user")

class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    food_type = Column(String, nullable=False)
    food_id = Column(Integer, nullable=False)
    food_name = Column(String, nullable=False)

    quantity_grams = Column(Float, nullable=False)
    portion_label = Column(String, nullable=True)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    fiber = Column(Float, nullable=False)
    sugar = Column(Float, nullable=False)
    sat_fat = Column(Float, nullable=False)
    sodium_mg = Column(Float, nullable=False)

    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="logs")