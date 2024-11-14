# README

## Installation
The following instructions are for MacOS.
### Requirements
Python 3.13 recommended.
```
python -m venv venv  # create a venv
source venv/bin/activate  # activate venv
pip install -r requirements.txt  # install requirements into this venv
```
### Postgres
This application requires Postgres to be installed on the host machine.  Use the Postgers.app installation method found here: https://postgresapp.com/.
If you want, you can add postgres to your shell path by adding the line
```
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
```
to your shell profile.

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the fields appropriately.

### Create/migrate database
To create the initial database, run
```
python init_db.py
```
This will open the Postegres app (which will start the db if it's not already running), then create an new database (if it doesn't exist) with the name you set in `.env`.

To perform migrations, run
```
alembic upgrade head
```
