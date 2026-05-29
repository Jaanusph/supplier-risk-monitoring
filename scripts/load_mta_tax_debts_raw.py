import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text


RAW_FILE = Path("data/raw/maksuvolglaste_nimekiri.csv")
RAW_TABLE = "raw_mta_tax_debts"


def get_engine():
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

    return create_engine(database_url)


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Missing file: {RAW_FILE}. Run scripts/download_mta_tax_debts.py first."
        )

    print(f"Reading file: {RAW_FILE}")

    df = pd.read_csv(
        RAW_FILE,
        sep=";",
        dtype=str,
        encoding="utf-8",
    )

    df["loaded_at"] = pd.Timestamp.now(tz="UTC")

    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    engine = get_engine()
    inspector = inspect(engine)

    if inspector.has_table(RAW_TABLE):
        print(f"Table {RAW_TABLE} already exists. Truncating and appending new data.")
        with engine.begin() as connection:
            connection.execute(text(f"truncate table {RAW_TABLE}"))

        df.to_sql(
            RAW_TABLE,
            engine,
            if_exists="append",
            index=False,
        )
    else:
        print(f"Table {RAW_TABLE} does not exist. Creating it.")
        df.to_sql(
            RAW_TABLE,
            engine,
            if_exists="fail",
            index=False,
        )

    print(f"Loaded table: {RAW_TABLE}")


if __name__ == "__main__":
    main()
