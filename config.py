import os
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASS = "1919"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "Darkom-Data-Pipeline" 

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "darkom-annonces.csv")