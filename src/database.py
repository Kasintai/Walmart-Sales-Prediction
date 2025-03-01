from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

from sqlalchemy import Boolean

import os

# Define database URL (update with your PostgreSQL credentials)
# DATABASE_URL = "postgresql://myuser:mypassword@localhost/walmart_sales"

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost/walmart_sales")
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres1:Kasintai1234@<RDS_ENDPOINT>:5432/database-1")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres1:Kasintai1234@database-1.c5imekk40mz4.ap-southeast-2.rds.amazonaws.com:5432/mydb1")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define Predictions table
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_number = Column(Integer, nullable=False)
    department_number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    # is_holiday = Column(String, nullable=False)
    is_holiday = Column(Boolean, nullable=False)
    predicted_sales = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables in the database
Base.metadata.create_all(engine)


import logging
logging.basicConfig(level=logging.DEBUG)

# # Function to save a prediction to the database
# def save_prediction(store_number, department_number, date, is_holiday, predicted_sales):
#     session = SessionLocal()

#     # Convert numpy.int64 to standard Python int
#     store_number = int(store_number)
#     department_number = int(department_number)
#     predicted_sales = round(float(predicted_sales), 2)  # Ensures float compatibility
#     # is_holiday = bool(is_holiday)  # Convert numpy.bool_ to standard Python bool

#     # ✅ Ensure `is_holiday` is stored as a BOOLEAN, not a string
#     if isinstance(is_holiday, str):
#         is_holiday = True if is_holiday.lower() == "true" else False
#     else:
#         is_holiday = bool(is_holiday)
    
#     logging.debug(f"Saving prediction: Store={store_number}, Dept={department_number}, Date={date}, Holiday={is_holiday}, Sales={predicted_sales}")

#     new_entry = Prediction(
#         store_number=store_number,
#         department_number=department_number,
#         date=date,
#         is_holiday=is_holiday,
#         predicted_sales=predicted_sales
#     )
#     session.add(new_entry)
#     session.commit()
#     session.close()

import threading

lock = threading.Lock()  # ✅ Prevent race conditions

def save_prediction(store_number, department_number, date, is_holiday, predicted_sales):
    with lock:  # ✅ Ensure only one request is processed at a time
        session = SessionLocal()

        store_number = int(store_number)
        department_number = int(department_number)
        predicted_sales = round(float(predicted_sales), 2)
        is_holiday = bool(is_holiday)

        logging.debug(f"Saving prediction: Store={store_number}, Dept={department_number}, Date={date}, Holiday={is_holiday}, Sales={predicted_sales}")

        new_entry = Prediction(
            store_number=store_number,
            department_number=department_number,
            date=date,
            is_holiday=is_holiday,
            predicted_sales=predicted_sales
        )
        session.add(new_entry)
        session.commit()
        session.close()


    # # ✅ Check if a similar prediction already exists
    # existing_entry = session.query(Prediction).filter_by(
    #     store_number=store_number,
    #     department_number=department_number,
    #     date=date,
    #     is_holiday=is_holiday,
    #     predicted_sales=predicted_sales  # Ensure the same prediction value is not saved twice
    # ).first()

    # if not existing_entry:  # Only save if there's no existing entry
    #     new_entry = Prediction(
    #         store_number=store_number,
    #         department_number=department_number,
    #         date=date,
    #         is_holiday=is_holiday,
    #         predicted_sales=predicted_sales
    #     )
    #     session.add(new_entry)
    #     session.commit()

    # session.close()

# Function to retrieve all predictions from the database
def get_predictions():
    session = SessionLocal()
    predictions = session.query(Prediction).all()
    session.close()

    # ✅ Ensure `is_holiday` is properly converted to a boolean
    for p in predictions:
        if isinstance(p.is_holiday, str):
            p.is_holiday = True if p.is_holiday.lower() == "true" else False
    
    # # ✅ Remove duplicates before returning (if any)
    # unique_predictions = {(
    #     p.store_number, 
    #     p.department_number, 
    #     p.date, 
    #     p.is_holiday, 
    #     p.predicted_sales
    # ): p for p in predictions}.values()

    return predictions
    # return list(unique_predictions)

#####
from sqlalchemy.sql import text # Import text function

def refresh_table():
    session = SessionLocal()
    session.execute(text("TRUNCATE TABLE predictions RESTART IDENTITY;")) # Wrap SQL command in text()
    session.commit()
    session.close()

