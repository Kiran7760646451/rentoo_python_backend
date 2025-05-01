import pymysql
from .config import Config
import logging

logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise Exception(f"Database connection failed: {str(e)}")
