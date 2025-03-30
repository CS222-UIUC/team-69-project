import psycopg2
from dotenv import dotenv_values
import os
from datetime import datetime
import sys

from dummydata import generate_users, insert_users
from matchingalgo import (
    fetch_users_from_db,
    match_all_requests
)

def reset_db(cursor):
    print("Resetting DB...")

    cursor.execute("DELETE FROM matches;")
    cursor.execute("DELETE FROM match_requests;")
    cursor.execute("DELETE FROM oauth_users;")
    cursor.execute("DELETE FROM users;")

    cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE oauth_users_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE match_requests_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE matches_id_seq RESTART WITH 1;")

def insert_match_requests_for_all(cursor):
    cursor.execute("SELECT id, classes_needed FROM users;")
    users = cursor.fetchall()

    for user_id, needed_classes in users:
        for subject in needed_classes:
            cursor.execute(
                "INSERT INTO match_requests (student_id, requested_subject, created_at) VALUES (%s, %s, NOW());",
                (user_id, subject)
            )

def main():
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

    # Step 1: Reset DB
    reset_db(cursor)

    # Step 2: Generate and insert users
    insert_users(generate_users(30), cursor, conn)

    # Step 3: Insert match requests for each subject needed by each user
    insert_match_requests_for_all(cursor)
    conn.commit()

    # Step 4: Perform matching for all requests with progress tracker
    total_requests = cursor.execute("SELECT COUNT(*) FROM match_requests;")
    cursor.execute("SELECT COUNT(*) FROM match_requests;")
    total = cursor.fetchone()[0]

    def progress_tracker(matched_count):
        sys.stdout.write(f"\rMatching requests... ({matched_count}/{total})")
        sys.stdout.flush()

    match_all_requests(cursor, conn, progress_callback=progress_tracker)

    print("\nAll matches completed.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
