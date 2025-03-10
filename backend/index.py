from dotenv import dotenv_values
import psycopg2
import os

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}


def read_sql_file(path):
    sql_script = ""
    with open(path) as f:
        sql_script = f.read()
    return sql_script


create_user_tables_script = read_sql_file("users.sql")

conn = psycopg2.connect(
    database=config["POSTGRES_DATABASE_NAME"],
    host=config["POSTGRES_DATABASE_HOST"],
    user=config["POSTGRES_DATABASE_USER"],
    password=config["POSTGRES_DATABASE_PASSWORD"],
    port=config["POSTGRES_DATABASE_PORT"],
)

cursor = conn.cursor()
cursor.execute(create_user_tables_script)
conn.commit()

cursor.close()
conn.close()
