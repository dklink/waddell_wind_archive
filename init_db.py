import os
import subprocess
from time import sleep
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql


def launch_postgres():
    subprocess.run(["open", "/Applications/Postgres.app"])
    print("Waiting for postgres to launch...")
    sleep(0.5)


def create_database(dbname, user, password, host="localhost", port="5432"):
    print(f"Creating database '{dbname}'...")
    try:
        connection = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        connection.autocommit = True  # Needed for database creation

        # Open a cursor to perform database operations and automatically close when done
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"Database '{dbname}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{dbname}' already exists.")
    finally:
        connection.close()


def run_migrations():
    pass


if __name__ == "__main__":
    load_dotenv()
    launch_postgres()
    create_database(
        dbname="waddell_wind_archive",
        user=os.environ["db_username"],
        password=os.environ["db_password"],
    )
