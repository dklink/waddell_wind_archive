# An archive script for a web image link.
# Pulls the latest image, persists it in local filesystem,
#  and writes metadata to a postgresql database.
# Assumes database has already been initialized and migrated.

import sys
from datetime import datetime, timezone

import requests

sys.path.append("../common")

from common.database import SessionLocal
from common.image_store import IMAGE_STORE_PATH
from common.models import Images

LIVE_WADDELL_WIND_URL = "https://mapper.weatherflow.com/cgi-bin/tinyGv2Wap.gif?t=213&d=t&c=0&cb=41741&wid=1&width=900&height=220&sh=0&eh=23"


def archive_image():
    # 1. download image to local filesystem
    if not IMAGE_STORE_PATH.exists():
        IMAGE_STORE_PATH.mkdir(parents=True)

    img_data = requests.get(LIVE_WADDELL_WIND_URL).content
    archived_at = datetime.now(timezone.utc)
    print(f"Image successfully downloaded at timestamp {archived_at.timestamp()}")

    img_path = IMAGE_STORE_PATH / f"{int(archived_at.timestamp())}.gif"
    with open(img_path, "wb") as handler:
        handler.write(img_data)
    print(f"Image successfully written to disk at {img_path}")

    # 2. write metadata into DB
    with SessionLocal() as session:
        new_image = Images(
            archived_at=archived_at,
            filename=str(img_path.name),
        )
        session.add(new_image)
        session.commit()

        print(f"New image metadata added to DB with ID: {new_image.id}")


if __name__ == "__main__":
    archive_image()
