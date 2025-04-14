import psycopg2
from datetime import datetime
from dotenv import dotenv_values
import os

# Load from .env and .env.development.local
config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}

def connect_db():
    return psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )

def get_display_name(cursor, user_id):
    cursor.execute("SELECT display_name FROM users WHERE id = %s;", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else "Unknown User"

def show_chat(cursor, match_id):
    cursor.execute("""
        SELECT sender_id, message_text, created_at 
        FROM chat_messages 
        WHERE match_id = %s 
        ORDER BY created_at ASC;
    """, (match_id,))
    messages = cursor.fetchall()

    print("\n=== Chat History ===\n")
    for sender_id, text, timestamp in messages:
        sender = get_display_name(cursor, sender_id)
        ts = timestamp.strftime("%Y-%m-%d %H:%M")
        print(f"[{ts}] {sender}: {text}")
    print("\n====================\n")

def send_message(cursor, match_id, sender_id, message):
    cursor.execute("""
        INSERT INTO chat_messages (match_id, sender_id, message_text, created_at)
        VALUES (%s, %s, %s, NOW());
    """, (match_id, sender_id, message))

def main():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        match_id = int(input("Enter match ID: ").strip())
        sender_id = int(input("Enter your user ID: ").strip())
        show_chat(cursor, match_id)

        print("Type your messages below. Type 'exit' to leave the chat.\n")

        while True:
            message = input("You: ")
            if message.lower() == "exit":
                break
            if message.strip():
                send_message(cursor, match_id, sender_id, message)
                conn.commit()
                show_chat(cursor, match_id)

    finally:
        cursor.close()
        conn.close()
        print("Chat session ended.")

if __name__ == "__main__":
    main()
