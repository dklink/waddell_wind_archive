import os

import psycopg2
from psycopg2 import sql


def create_database(dbname, user, password, host, port="5432"):
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


if __name__ == "__main__":
    create_database(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_PUBLIC_IP"],
    )
