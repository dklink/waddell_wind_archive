docker run \
    --env-file .env \
    -p 5000:5000 \
    -v /Users/dklink/Desktop/waddell_images:/waddell_wind/images \
    waddell_wind_backend
