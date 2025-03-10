from dotenv import dotenv_values
import psycopg2
import os

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}

sql_script = ""
with open("users.sql") as f:
    sql_script = f.read()

conn = psycopg2.connect(
    database=config["POSTGRES_DATABASE_NAME"],
    host=config["POSTGRES_DATABASE_HOST"],
    user=config["POSTGRES_DATABASE_USER"],
    password=config["POSTGRES_DATABASE_PASSWORD"],
    port=config["POSTGRES_DATABASE_PORT"],
)

cursor = conn.cursor()
cursor.execute(sql_script)
conn.commit()

cursor.close()
conn.close()
