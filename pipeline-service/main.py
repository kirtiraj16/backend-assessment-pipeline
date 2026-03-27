from fastapi import FastAPI
from ingestion import run_pipeline
from database import engine
from model import Base, Customer   # ✅ VERY IMPORTANT

app = FastAPI()

@app.on_event("startup")
def startup():
    print("🔥 Creating tables...")
    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Pipeline Service Running"}


@app.get("/ingest")
def ingest():
    try:
        count = run_pipeline()
        return {
            "status": "success",
            "records_processed": count
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }