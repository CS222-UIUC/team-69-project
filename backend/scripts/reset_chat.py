import psycopg2
from dotenv import dotenv_values
import os

def reset_chat_table():
    print("🧹 Resetting chat_messages table...")

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

    cursor.execute("""
        DROP TABLE IF EXISTS chat_messages CASCADE;
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
            sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            message_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    print("✅ chat_messages table reset complete.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    reset_chat_table()
