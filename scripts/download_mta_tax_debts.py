import os
from pathlib import Path

import requests
from dotenv import load_dotenv


RAW_DIR = Path("data/raw")
OUTPUT_FILE = RAW_DIR / "maksuvolglaste_nimekiri.csv"


def main() -> None:
    load_dotenv(dotenv_path=Path(".env"))

    url = os.getenv("MTA_TAX_DEBTS_URL")
    if not url:
        raise RuntimeError("MTA_TAX_DEBTS_URL is missing from .env")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading MTA tax debts from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    OUTPUT_FILE.write_bytes(response.content)

    print(f"Saved file: {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size} bytes")


if __name__ == "__main__":
    main()
