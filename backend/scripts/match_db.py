import psycopg2
from dotenv import dotenv_values
import os
import sys

from matchingalgo import match_all_requests

def main():
    # Load database config from environment
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development.local"),
        **os.environ,
    }

    # Establish DB connection
    conn = psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )
    cursor = conn.cursor()

    # Count total match requests in the DB
    cursor.execute("SELECT COUNT(*) FROM match_requests;")
    total = cursor.fetchone()[0]

    # Real-time tracker in terminal – low-tech but works
    def progress_tracker(matched_count):
        sys.stdout.write(f"\rMatching requests... ({matched_count}/{total})")
        sys.stdout.flush()

    # Run the matching algorithm
    match_all_requests(cursor, conn, progress_callback=progress_tracker)

    print("\nAll matches completed.")  # good job, database
    cursor.close()
    conn.close()  # always clean up

if __name__ == "__main__":
    main()
