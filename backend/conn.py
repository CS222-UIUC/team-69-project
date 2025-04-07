import os
from dotenv import dotenv_values
import psycopg2


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
