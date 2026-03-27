import requests
from database import SessionLocal
from model import Customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FLASK_API = "http://mock-server:5000/api/customers"


def fetch_all_data():
    logger.info("Fetching data from API...")

    response = requests.get(FLASK_API)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from API")

    data = response.json()

    logger.info(f"Total records fetched: {len(data)}")
    return data


def save_to_db(customers):
    db = SessionLocal()
    count = 0

    try:
        for c in customers:
            # ✅ Check existing record
            existing = db.query(Customer).filter_by(customer_id=c.get("id")).first()

            if existing:
                # ✅ Update
                existing.first_name = c.get("first_name")
                existing.last_name = c.get("last_name")
                existing.email = c.get("email")
            else:
                # ✅ Insert
                new_customer = Customer(
                    customer_id=c.get("id"),
                    first_name=c.get("first_name"),
                    last_name=c.get("last_name"),
                    email=c.get("email")
                )
                db.add(new_customer)

            count += 1

        db.commit()
        logger.info(f"{count} records processed")

    except Exception as e:
        db.rollback()
        logger.error(f"Error: {str(e)}")

    finally:
        db.close()

    return count


def run_pipeline():
    logger.info("Starting data ingestion pipeline...")

    data = fetch_all_data()

    if not data:
        logger.warning("No data received")
        return 0

    count = save_to_db(data)

    logger.info("Pipeline completed successfully")
    return count