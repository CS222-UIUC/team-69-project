import openai
from flask_socketio import join_room, leave_room, send
from datetime import datetime
from psycopg2 import connect
from dotenv import dotenv_values
from flask import session
import os
from dotenv import load_dotenv
from scripts.matchingalgo import parse_pg_array

from conn import config, conn


# === Connect to DB ===
def connect_db():
    # === Environment Configuration ===

    # return connect(
    #     database=config["POSTGRES_DATABASE_NAME"],
    #     host=config["POSTGRES_DATABASE_HOST"],
    #     user=config["POSTGRES_DATABASE_USER"],
    #     password=config["POSTGRES_DATABASE_PASSWORD"],
    #     port=config["POSTGRES_DATABASE_PORT"],
    # )
    return conn


from openai import OpenAI
from datetime import datetime

load_dotenv(dotenv_path=".env.development.local")

# Set up OpenAI client with the key from env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


client = OpenAI()


def generate_starter_message(user1_id, user2_id, match_id, save_to_db=True):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, display_name, major, year, classes_can_tutor, classes_needed
        FROM users
        WHERE id IN (%s, %s);
    """,
        (user1_id, user2_id),
    )
    users = cur.fetchall()
    if len(users) != 2:
        cur.close()
        return "other", "Hi there! Excited to connect with you!"

    user1, user2 = users
    user1_display_name = user1[1]
    user2_display_name = user2[1]
    user1_first_name = (
        user1_display_name.split()[0].capitalize() if user1_display_name else "I"
    )

    user1_classes = set(parse_pg_array(user1[4]) + parse_pg_array(user1[5]))
    user2_classes = set(parse_pg_array(user2[4]) + parse_pg_array(user2[5]))
    shared_classes = list(user1_classes & user2_classes)

    shared_major = user1[2] == user2[2] and user1[2]
    shared_year = user1[3] == user2[3] and user1[3]

    prompt_parts = []
    if shared_classes:
        prompt_parts.append(
            f"You both are connected through classes like {', '.join(shared_classes)}."
        )
    if shared_major:
        prompt_parts.append(f"You also share the same major: {shared_major}.")
    if shared_year:
        prompt_parts.append(f"You are both {shared_year}s.")

    prompt_context = " ".join(prompt_parts)
    if not prompt_context:
        prompt_context = "You matched with a fellow student at your university."

    full_prompt = f"""
You are helping a university student named {user1_first_name} break the ice in a chat with another student named {user2_display_name}.

Context:
{prompt_context}

Write a **friendly, short, casual first message** that:
- Starts by introducing yourself ("Hey, I'm {user1_first_name}!")
- Mentions common classes/major/year if relevant
- Stays within **2-3 lines maximum**
- No emojis, no jokes, no quotes.

Keep the tone friendly and respectful.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, casual university student writing short, friendly messages.",
                },
                {"role": "user", "content": full_prompt},
            ],
            temperature=0.6,
            max_tokens=100,
        )

        starter_message = response.choices[0].message.content.strip()

        if save_to_db and starter_message:
            cur.execute(
                """
                INSERT INTO chat_messages (match_id, sender_id, message_text, created_at)
                VALUES (%s, %s, %s, %s);
            """,
                (match_id, user1[0], starter_message, datetime.now()),
            )
            conn.commit()

        cur.close()

        return user1_display_name, starter_message

    except Exception as e:
        print(f"ChatGPT Error: {e}")
        cur.close()
        return (
            user1_display_name,
            f"Hi, I'm {user1_first_name}! Excited to connect with you!",
        )


# === DB Utilities ===
def get_display_name(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT display_name FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()
    cur.close()
    return row[0] if row else f"User {user_id}"


def fetch_messages(match_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sender_id, message_text, created_at
        FROM chat_messages
        WHERE match_id = %s
        ORDER BY created_at ASC;
    """,
        (match_id,),
    )
    messages = cur.fetchall()
    cur.close()
    return [
        {"sender": get_display_name(sender), "message": msg}
        for sender, msg, _ in messages
    ]


def insert_message(match_id, sender_id, text):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO chat_messages (match_id, sender_id, message_text, created_at)
        VALUES (%s, %s, %s, %s);
    """,
        (match_id, sender_id, text, datetime.now()),
    )
    conn.commit()
    cur.close()


def get_matches_for_user(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT u.id, u.display_name, 'You matched with them' AS direction
        FROM matches m
        JOIN users u ON u.id = m.matched_user_id
        WHERE m.requester_id = %s

        UNION

        SELECT u.id, u.display_name, 'They matched with you' AS direction
        FROM matches m
        JOIN users u ON u.id = m.requester_id
        WHERE m.matched_user_id = %s;
    """,
        (user_id, user_id),
    )
    results = [
        {"id": uid, "name": name, "direction": direction}
        for uid, name, direction in cur.fetchall()
    ]
    cur.close()
    return results


def get_match_id_between(user1_id, user2_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id FROM matches
        WHERE requester_id = %s AND matched_user_id = %s
        LIMIT 1;
    """,
        (user1_id, user2_id),
    )
    row = cur.fetchone()

    if not row:
        cur.execute(
            """
            SELECT id FROM matches
            WHERE requester_id = %s AND matched_user_id = %s
            LIMIT 1;
        """,
            (user2_id, user1_id),
        )
        row = cur.fetchone()

    cur.close()
    return row[0] if row else None


# === Register Socket.IO Events ===
def init_chat_events(socketio):

    @socketio.on("connect")
    def handle_connect():
        user_id = session.get("user_id")
        match_id = session.get("match_id")
        if not user_id or not match_id:
            return
        join_room(match_id)
        send(
            {
                "sender": "",
                "message": f"{get_display_name(user_id)} has entered the chat",
            },
            to=match_id,
        )

    @socketio.on("message")
    def handle_message(data):
        user_id = session.get("user_id")
        match_id = session.get("match_id")

        if not user_id or not match_id:
            return
        insert_message(match_id, user_id, data["message"])

        send(
            {"sender": get_display_name(user_id), "message": data["message"]},
            to=match_id,
        )

    @socketio.on("disconnect")
    def handle_disconnect():
        user_id = session.get("user_id")
        match_id = session.get("match_id")
        if not user_id or not match_id:
            return
        leave_room(match_id)
        # send(
        #     {"sender": "", "message": f"{get_display_name(user_id)} has left the chat"},
        #     to=match_id,
        # )

    @socketio.on("regenerate_starter")
    def handle_regenerate_starter(data):
        user_id = session.get("user_id")
        match_id = session.get("match_id")
        other_user_id = data.get("other_user_id")

        if not user_id or not match_id or not other_user_id:
            return

        sender, new_starter_message = generate_starter_message(
            user_id, other_user_id, match_id, save_to_db=True
        )

        send(
            {"sender": sender, "message": new_starter_message, "type": "starter"},
            to=match_id,
        )
