import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    load_dotenv(dotenv_path=Path(".env"))

    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    database_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    engine = create_engine(database_url)

    with engine.connect() as connection:
        result = connection.execute(text("select current_database(), current_user"))
        database_name, current_user = result.one()

    print("Database connection OK")
    print(f"Host: {db_host}")
    print(f"Database: {database_name}")
    print(f"User: {current_user}")


if __name__ == "__main__":
    main()
