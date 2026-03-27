from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/customer_db"
# 🔥 Retry connection
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        print("✅ Database connected")
        break
    except Exception as e:
        print("⏳ Waiting for DB...", e)
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to database")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()