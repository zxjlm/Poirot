import logging
import os

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    os.environ["MYSQL"] = ""
    os.environ["MYSQL_DB"] = "fastapi_demo"
    os.environ["MYSQL_HOST"] = "db"
    os.environ["MYSQL_PASSWORD"] = "root"
    os.environ["MYSQL_PORT"] = "3306"
    os.environ["MYSQL_ROOT_PASSWORD"] = "root"
    os.environ["MYSQL_USER"] = "root"
    main()
