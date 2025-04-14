import psycopg2 #pip install --only-binary :all: psycopg2-binary
from dotenv import dotenv_values
import os

def run_sql_file(cursor, filename):
    with open(filename, 'r') as file:
        sql = file.read()
        cursor.execute(sql)

if __name__ == "__main__":
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development.local"),
        **os.environ,
    }

    conn = psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )
    cursor = conn.cursor()

    run_sql_file(cursor, "users.sql")
    run_sql_file(cursor, "matches.sql")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database schema set up successfully!")
