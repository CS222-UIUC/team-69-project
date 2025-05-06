# reset_db.py

import psycopg2
from dotenv import dotenv_values
import os
from datetime import datetime

from dummydata import generate_users, insert_users


# Wipe all user-related data and reset counters
def reset_db(cursor):
    print("Resetting DB...")

    cursor.execute("DELETE FROM matches;")  # clear old matches
    cursor.execute("DELETE FROM match_requests;")  # clear past requests
    cursor.execute("DELETE FROM oauth_users;")  # clear login data
    cursor.execute("DELETE FROM users;")  # wipe all users

    # Reset all auto-incrementing IDs (start fresh)
    cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE oauth_users_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE match_requests_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE matches_id_seq RESTART WITH 1;")


import sys
from psycopg2.extras import execute_values


# Add match requests for every subject a user needs help with
def insert_match_requests_for_all(cursor):
    print("Inserting match requests...")

    cursor.execute("SELECT id, classes_needed FROM users;")
    users = cursor.fetchall()

    all_requests = []
    total = len(users)

    for i, (user_id, needed_classes) in enumerate(users, start=1):
        for subject in needed_classes:
            all_requests.append((user_id, subject))  # each subject = one match request

    execute_values(
        cursor,
        """
        INSERT INTO match_requests (student_id, requested_subject, created_at)
        VALUES %s
        """,
        [(uid, subject, datetime.now()) for uid, subject in all_requests],
    )

    print(
        f"Inserted {len(all_requests)} match requests."
    )  # that’s a lot of asking for help


def main():
    # Load env variables from .env files + OS
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development.local"),
        **os.environ,
    }

    # Connect to DB using psycopg2
    conn = psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )
    cursor = conn.cursor()

    # Run reset and re-seed process
    reset_db(cursor)
    insert_users(generate_users(500), cursor, conn)  # plug in 100 fresh users
    insert_match_requests_for_all(cursor)

    conn.commit()
    print("DB Reset + Users & Match Requests Inserted")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
