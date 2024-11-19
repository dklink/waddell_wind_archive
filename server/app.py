from datetime import datetime, timezone

from flask import Flask, abort, request, send_file
from sqlalchemy import func

from common.database import SessionLocal
from common.image_store import IMAGE_STORE_PATH
from common.models import Images

app = Flask(__name__)

LOCAL_DEV = False


@app.route("/images/nearest", methods=["GET"])
def get_nearest_image():
    """
    Retrieve the image nearest to a given timestamp.

    This endpoint accepts a timestamp as a query parameter and returns metadata
    for the image archived closest to the specified timestamp. If the timestamp
    is missing, invalid, or no images are found, appropriate error messages are returned.

    Query Parameters:
    -----------------
    timestamp : float (required)
        The Unix timestamp (in seconds) to find the nearest image.

    Returns:
        The image file or an appropriate error message
    """
    # Get the 'timestamp' query parameter
    timestamp = request.args.get("timestamp")
    if not timestamp:
        abort(400, "Missing 'timestamp' query parameter")

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
        image_filename = nearest_image.filename
        image_path = IMAGE_STORE_PATH / image_filename
        if not image_path.is_file():
            abort(404, description=f"Image file not found at expected path.")

        # Return the image file using send_file
        return send_file(
            image_path,
            mimetype="image/gif",
            as_attachment=False,  # Set to True to prompt download
        )


if __name__ == "__main__":
    app.run(debug=True)
