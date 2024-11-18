from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, send_file
from sqlalchemy import func

from src.database.db import SessionLocal
from src.database.models import Images

app = Flask(__name__)


@app.route("/get/<timestamp>", methods=["GET"])
def get_nearest_image(timestamp):
    """
    Fetch the image nearest to the given timestamp and return the image file.

    Args:
        timestamp (str): A Unix timestamp (seconds since epoch).

    Returns:
        The image file or 404 if no images are found.
    """
    try:
        # Convert the input timestamp to a datetime object
        target_time = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
    except ValueError:
        abort(400, description="Invalid timestamp format. Use a Unix timestamp.")

    # Query the database for the nearest image
    with SessionLocal() as session:
        nearest_image = (
            session.query(Images)
            .order_by(
                func.abs(func.extract("epoch", Images.archived_at - target_time))
            )  # Convert interval to seconds to allow use of ABS
            .first()
        )

        if not nearest_image:
            abort(404, description="No images found in the database.")

        # Check if the image file exists
        image_path = Path(nearest_image.image_path)
        if not image_path.is_file():
            abort(404, description=f"Image file not found at expected path.")

        # Return the image file using send_file
        return send_file(
            image_path,
            mimetype="image/gif",
            as_attachment=False,  # Set to True to prompt download
        )


if __name__ == "__main__":
    app.run()
