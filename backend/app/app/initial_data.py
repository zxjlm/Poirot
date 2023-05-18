import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    pass


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    # os.environ["MYSQL"] = ""
    # os.environ["MYSQL_DB"] = "fastapi_demo"
    # os.environ["MYSQL_HOST"] = "db"
    # os.environ["MYSQL_PASSWORD"] = "root"
    # os.environ["MYSQL_PORT"] = "3306"
    # os.environ["MYSQL_ROOT_PASSWORD"] = "root"
    # os.environ["MYSQL_USER"] = "root"
    main()
