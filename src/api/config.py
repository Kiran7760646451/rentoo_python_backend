import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "mysql")
    DB_NAME = os.getenv("DB_NAME", "rentoo")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
