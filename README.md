# README

## Installation
The following instructions are for MacOS.
### Requirements
Python 3.13 recommended.  System components are meant to be used via docker - but for local development, you can install requirements like so:
```
python -m venv venv_archiver  # create a venv for just the archiver
source venv_archiver/bin/activate  # activate venv
pip install -r archiver/requirements.txt
pip install -r requirements-dev.txt
```
And something similar can be done for doing development work on the server.
### Postgres
This application requires Postgres to be installed on the host machine.  Use the Postgers.app installation method found here: https://postgresapp.com/.
Then add the command line tools to your path:
```
sudo mkdir -p /etc/paths.d &&
echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
```
to your shell profile.

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the fields appropriately.  You may need to run
```
source .env
```
before any scripts which rely on the variables defined in there.

### Create/migrate database
To create the initial database, run
```
source .env
python -m common.utils.init_db
```
This will open the Postegres app (which will start the db if it's not already running), then create an new database (if it doesn't exist) with the name you set in `.env`.

To perform migrations, navigate to `common/migrations` and run
```
alembic upgrade head
```
To generate new migrations dynamically, run
```
alembic revision --autogenerate
```

## Usage
### Image archiver
To archive an image:
```
docker-compose build archiver  # only need to do once
docker-compose up archiver
```

(or to do it locally:)
```
source .env  # uncomment the proper variables in there before this
python -m archiver.archive_image
```

You can verify that a new image exists in your local image store, and that the database has a new row.

### Backend App
The backend app exposes an API with a `/get/<timestamp>` that returns the nearest image to that timestamp in the database.


To start the server:
```
docker-compose build server  # only need to do once
docker-compose up server
```

Or locally:
```
source .env  # after modifying it appropriately
python -m server.app
```

Exercise the server by visiting
`http://127.0.0.1:5000/get/<timestamp>` in a browser.  Insert a recent unix timestamp (e.g. 1731955206), and you should see the nearest archived image!
