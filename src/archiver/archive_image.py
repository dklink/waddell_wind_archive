# An archive script for a web image link.
# Pulls the latest image, persists it in local filesystem,
#  and writes metadata to a postgresql database.
# Assumes database has already been initialized and migrated.

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.archiver.constants import LIVE_WADDELL_WIND_URL
from src.database import start_db_script
from src.database.db import SessionLocal
from src.database.models import Images


def archive_image():
    # 1. download image to local filesystem
    image_store = Path(os.environ["IMAGE_STORE_PATH"])
    if not image_store.exists():
        image_store.mkdir(parents=True)

    img_data = requests.get(LIVE_WADDELL_WIND_URL).content
    archived_at = datetime.now(timezone.utc)
    print(f"Image successfully downloaded at timestamp {archived_at.timestamp()}")

    img_path = image_store / f"{int(archived_at.timestamp())}.gif"
    with open(img_path, "wb") as handler:
        handler.write(img_data)
    print(f"Image successfully written to disk at {img_path}")

    # 2. write metadata into DB
    with SessionLocal() as session:
        new_image = Images(
            archived_at=archived_at,
            image_path=str(img_path),
        )
        session.add(new_image)
        session.commit()

        print(f"New image metadata added to DB with ID: {new_image.id}")


if __name__ == "__main__":
    subprocess.run(["sh", start_db_script])
    archive_image()
