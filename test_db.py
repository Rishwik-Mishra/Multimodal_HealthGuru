from database.session import SessionLocal
from database.models import Food

db = SessionLocal()
print(db.query(Food).count())
