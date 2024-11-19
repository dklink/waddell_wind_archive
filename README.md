# README

## Installation
The following instructions are for MacOS.
### Requirements
Python 3.13 recommended.  For setup, we'll need to set up a minimal dev environment:
```
python -m venv venv_dev
source venv_dev/bin/activate
pip install -r requirements-dev.txt
```
### Postgres
This application requires Postgres to be installed on the host machine.  Use the Postgers.app installation method found here: https://postgresapp.com/.
Then add the command line tools to your path by running the following lines:
```
sudo mkdir -p /etc/paths.d &&
echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
```

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the fields appropriately.

### Create/migrate database
To create the initial database, make sure you've launched the Postgres app and that the database is running.  Then, run
```
source .env
python -m common.utils.init_db
```
This will create an new database (if it doesn't exist) with the name you set in `.env`.

To perform migrations, navigate to `common/migrations` and run
```
alembic upgrade head
```

### Docker
You'll also need docker.  Go install Docker Desktop if you don't already have it.


## Usage
### Image archiver
To archive an image:
```
docker-compose build archiver  # only need to do once
docker-compose up archiver
```

You can verify that a new image exists in your local image store, and that the database has a new row.

### Backend App
The backend app exposes an API with a `/get/<timestamp>` that returns the nearest image to that timestamp in the database.


To start the server:
```
docker-compose build server  # only need to do once
docker-compose up server
```

Exercise the server by visiting
`http://127.0.0.1:5000/get/<timestamp>` in a browser.  Insert a recent unix timestamp (e.g. 1731955206), and you should see the nearest archived image!

## Development
If you make changes to the database, you can generate new migrations by navigating to `common/migrations` and running
```
alembic revision --autogenerate
```

If you want to run the components locally, you'll need to modify your `.env` file according to the comments therein.  Then,
```
source .env
python -m archiver.archive_image
# or,
python -m server.app
```